from __future__ import annotations
import os
import datetime
import logging
import uuid
from typing import Optional, List, Dict, Any, TypeVar
from contextlib import contextmanager

from sqlalchemy import create_engine, UniqueConstraint, text, Column, Integer, String, ForeignKey, Text, DateTime, Table, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from slugify import slugify

ModelType = TypeVar('ModelType')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base exception for database operations."""
    pass

class NotFoundError(DatabaseError):
    """Raised when a requested resource is not found."""
    pass

class ConfigurationError(DatabaseError):
    """Raised for configuration related errors."""
    pass

class ValidationError(DatabaseError):
    """Raised for data validation errors."""
    pass

class DatabaseConfig:
    """Database configuration settings."""
    
    DATABASE_URI: str = os.getenv('DATABASE_URI', 'postgresql://myuser:mypassword@localhost:5433/mydatabase')
    POOL_SIZE: int = int(os.getenv('DB_POOL_SIZE', 10))
    MAX_OVERFLOW: int = int(os.getenv('DB_MAX_OVERFLOW', 20))
    POOL_TIMEOUT: int = int(os.getenv('DB_POOL_TIMEOUT', 60))
    POOL_RECYCLE: int = int(os.getenv('DB_POOL_RECYCLE', 1800))
    ECHO: bool = os.getenv('DB_ECHO', 'false').lower() == 'true'

    @classmethod
    def validate(cls) -> None:
        """Validate database configuration."""
        if not cls.DATABASE_URI:
            raise ConfigurationError("DATABASE_URI must be configured")

Base = declarative_base()

class BaseModel(Base):
    """Base model with common fields."""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    public_id = Column(String(36), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    slug = Column(String(100), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __init__(self, **kwargs):
        if hasattr(self, 'generate_slug'):
            self.slug = self.generate_slug(**kwargs)
        super().__init__(**kwargs)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'public_id': self.public_id,
            'slug': self.slug,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'is_active': self.is_active
        }

    @staticmethod
    def slugify(text: str) -> str:
        """Generate a slug from text."""
        return slugify(text, max_length=100, word_boundary=True, save_order=True)

# Association table with audit fields
user_chats = Table('user_chats', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('chat_id', Integer, ForeignKey('chats.id'), primary_key=True),
    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('created_by', Integer, ForeignKey('users.id', name='fk_created_by'))
)

class User(BaseModel):
    __tablename__ = 'users'
    
    username = Column(String(30), unique=True, nullable=False, index=True)
    display_name = Column(String(50), nullable=False)
    profile = Column(Text)
    record_instructions = Column(Boolean, default=False)
    chats = relationship(
        'Chat',
        secondary=user_chats,
        primaryjoin="User.id == user_chats.c.user_id",
        secondaryjoin="Chat.id == user_chats.c.chat_id",
        back_populates='users'
    )
    
    def generate_slug(self, **kwargs) -> str:
        return self.slugify(kwargs.get('username', ''))

class Provider(BaseModel):
    __tablename__ = 'providers'
    
    name = Column(String(100), unique=True, nullable=False, index=True)
    api_endpoint = Column(String(255), nullable=False)
    api_key = Column(String(255))
    llms = relationship('LLM', back_populates='provider', cascade='all, delete-orphan')
    
    def generate_slug(self, **kwargs) -> str:
        return self.slugify(kwargs.get('name', ''))

class LLM(BaseModel):
    __tablename__ = 'llms'
    
    name = Column(String(100), nullable=False, index=True)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    provider = relationship('Provider', back_populates='llms')

    # Add unique constraint across name + provider_id
    __table_args__ = (
        UniqueConstraint('name', 'provider_id', name='uix_llm_name_provider'),
    )
    
    def generate_slug(self, **kwargs) -> str:
        provider_id = kwargs.get('provider_id')
        return self.slugify(f"{kwargs.get('name', '')}-{provider_id}")

class Chat(BaseModel):
    __tablename__ = 'chats'
    
    title = Column(String(100), nullable=False, index=True)
    users = relationship(
        'User',
        secondary=user_chats,
        primaryjoin="Chat.id == user_chats.c.chat_id",
        secondaryjoin="User.id == user_chats.c.user_id",
        back_populates='chats'
    )
    messages = relationship('Message', back_populates='chat', cascade='all, delete-orphan')
    
    def generate_slug(self, **kwargs) -> str:
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        return self.slugify(f"{kwargs.get('title', '')}-{timestamp}")

class Message(BaseModel):
    __tablename__ = 'messages'
    
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    llm_id = Column(Integer, ForeignKey('llms.id'))
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)
    
    user = relationship('User')
    chat = relationship('Chat', back_populates='messages')
    llm = relationship('LLM')
    
    def generate_slug(self, **kwargs) -> str:
        return self.slugify(f"msg-{datetime.datetime.now().timestamp()}")

class InstructionRecord(BaseModel):
    __tablename__ = 'instruction_records'
    
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    instruction = Column(String(100), nullable=False)
    
    user = relationship('User')
    chat = relationship('Chat')
    
    def generate_slug(self, **kwargs) -> str:
        return self.slugify(f"instr-{datetime.datetime.now().timestamp()}")

class DatabaseManageUnit:
    """Core database management class implementing the Repository pattern."""
    
    def __init__(self) -> None:
        """Initialize database connection and session factory."""
        DatabaseConfig.validate()
        
        self.engine = create_engine(
            DatabaseConfig.DATABASE_URI,
            pool_size=DatabaseConfig.POOL_SIZE,
            max_overflow=DatabaseConfig.MAX_OVERFLOW,
            pool_timeout=DatabaseConfig.POOL_TIMEOUT,
            pool_recycle=DatabaseConfig.POOL_RECYCLE,
            echo=DatabaseConfig.ECHO
        )
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.Session.remove()

    def init_db(self):
        """Initialize database schema."""
        try:
            with self.engine.connect() as connection:
                # Drop tables in correct order to handle dependencies
                for table in [
                    "user_chats",
                    "instruction_records",
                    "messages",
                    "chats",
                    "llms",
                    "providers",
                    "users"
                ]:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            
            Base.metadata.create_all(self.engine)
            logger.info("Database initialized successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise DatabaseError(f"Database initialization failed: {str(e)}")

    def reset_db(self):
        self.init_db()

    def soft_delete(self, entity: ModelType) -> None:
        """Soft delete entity."""
        with self.session_scope() as session:
            entity.is_active = False
            session.add(entity)

    def create_user(self, username: str, display_name: str, profile: str) -> Dict[str, Any]:
        """Create a user and return as dictionary."""
        with self.session_scope() as session:
            new_user = User(username=username, display_name=display_name, profile=profile, is_active=True)
            session.add(new_user)
            session.flush()  # Ensures new_user.public_id is available
            return self._user_to_dict(new_user)
    
    def update_user(self, public_id: str, username: Optional[str] = None, display_name: Optional[str] = None, profile: Optional[str] = None) -> Dict[str, Any]:
        """Update a user and return as dictionary."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            if username is not None:
                user.username = username
            if display_name is not None:
                user.display_name = display_name
            if profile is not None:
                user.profile = profile
            session.add(user)
            return self._user_to_dict(user)
    
    def delete_user(self, public_id: str) -> None:
        """Delete a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            self.soft_delete(user)
    
    def get_user_by_public_id(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get user by public_id as dictionary."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=public_id, is_active=True).first()
            return self._user_to_dict(user) if user else None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user by username as dictionary."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(username=username.lower(), is_active=True).first()
            return self._user_to_dict(user) if user else None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all active users as dictionaries."""
        with self.session_scope() as session:
            users = session.query(User).filter_by(is_active=True).all()
            return [self._user_to_dict(user) for user in users]

    def create_chat(self, title: str, user_public_ids: List[str]) -> Dict[str, Any]:
        """Create a chat with users and return as dictionary."""
        with self.session_scope() as session:
            chat = Chat(title=title)
            for public_id in user_public_ids:
                user = session.query(User).filter_by(public_id=public_id, is_active=True).first()
                if user:
                    chat.users.append(user)
            session.add(chat)
            session.flush()
            return self._chat_to_dict(chat)
    
    def update_chat(self, public_id: str, title: str) -> Dict[str, Any]:
        """Update a chat and return as dictionary."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=public_id, is_active=True).first()
            if not chat:
                raise NotFoundError("Chat not found")
            
            chat.title = title
            session.add(chat)
            return self._chat_to_dict(chat)
    
    def delete_chat(self, public_id: str) -> None:
        """Delete a chat."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=public_id, is_active=True).first()
            if not chat:
                raise NotFoundError("Chat not found")
            
            self.soft_delete(chat)
    
    def get_chat_by_public_id(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get chat by public_id as dictionary."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=public_id, is_active=True).first()
            return self._chat_to_dict(chat) if chat else None
    
    def get_chats_by_user(self, user_public_id: str) -> Optional[Dict[str, Any]]:
        """Get all chats for a user as dictionaries."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                return []
            
            chats = (session.query(Chat).join(Chat.users).filter(User.id == user.id).all())
            return [self._chat_to_dict(chat) for chat in chats]
    
    def get_all_chats(self) -> List[Dict[str, Any]]:
        """Get all active chats as dictionaries."""
        with self.session_scope() as session:
            chats = session.query(Chat).filter_by(is_active=True).all()
            return [self._chat_to_dict(chat) for chat in chats]

    def add_users_to_chat(self, chat_public_id: str, user_public_ids: List[str]) -> None:
        """Add users to a chat."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=chat_public_id, is_active=True).first()
            if not chat:
                raise NotFoundError("Chat not found")
            
            for public_id in user_public_ids:
                user = session.query(User).filter_by(public_id=public_id, is_active=True).first()
                if user:
                    chat.users.append(user)
            session.add(chat)
    
    def add_provider(self, name: str, api_endpoint: str, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Add a provider and return as dictionary."""
        with self.session_scope() as session:
            existing = session.query(Provider).filter_by(name=name, is_active=True).first()
            if existing:
                raise ValidationError(f"Provider '{name}' already exists")
            
            provider = Provider(name=name, api_endpoint=api_endpoint, api_key=api_key)
            session.add(provider)
            session.flush()
            return self._provider_to_dict(provider)
    
    def update_provider(self, public_id: str, name: Optional[str] = None, api_endpoint: Optional[str] = None, api_key: Optional[str] = None) -> Dict[str, Any]:
        """Update a provider and return as dictionary."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(public_id=public_id, is_active=True).first()
            if not provider:
                raise NotFoundError("Provider not found")
            
            if name is not None:
                provider.name = name
            if api_endpoint is not None:
                provider.api_endpoint = api_endpoint
            if api_key is not None:
                provider.api_key = api_key
            session.add(provider)
            return self._provider_to_dict(provider)
    
    def delete_provider(self, public_id: str) -> None:
        """Delete a provider."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(public_id=public_id, is_active=True).first()
            if not provider:
                raise NotFoundError("Provider not found")
            
            self.soft_delete(provider)
    
    def get_provider_by_public_id(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get provider by public_id as dictionary."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(public_id=public_id, is_active=True).first()
            return self._provider_to_dict(provider) if provider else None
    
    def get_provider_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get provider by name as dictionary."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(name=name, is_active=True).first()
            return self._provider_to_dict(provider) if provider else None
    
    def get_all_providers(self) -> List[Dict[str, Any]]:
        """Get all active providers as dictionaries."""
        with self.session_scope() as session:
            providers = session.query(Provider).filter_by(is_active=True).all()
            return [self._provider_to_dict(provider) for provider in providers]
    
    def add_llm(self, name: str, provider_public_id: str) -> Dict[str, Any]:
        """Add an LLM and return as dictionary."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(public_id=provider_public_id, is_active=True).first()
            if not provider:
                raise NotFoundError(f"Provider '{provider_public_id}' not found")
            
            existing = session.query(LLM).filter_by(name=name, provider_id=provider.id, is_active=True).first()
            if existing:
                raise ValidationError(f"LLM '{name}' already exists for provider '{provider.name}'")
            
            llm = LLM(name=name, provider_id=provider.id, provider=provider)
            session.add(llm)
            session.flush()
            return self._llm_to_dict(llm)
    
    def update_llm(self, public_id: str, name: str) -> Dict[str, Any]:
        """Update an LLM and return as dictionary."""
        with self.session_scope() as session:
            llm = session.query(LLM).filter_by(public_id=public_id, is_active=True).first()
            if not llm:
                raise NotFoundError("LLM not found")
            
            llm.name = name
            session.add(llm)
            return self._llm_to_dict(llm)
    
    def delete_llm(self, public_id: str) -> None:
        """Delete an LLM."""
        with self.session_scope() as session:
            llm = session.query(LLM).filter_by(public_id=public_id, is_active=True).first()
            if not llm:
                raise NotFoundError("LLM not found")
            
            self.soft_delete(llm)
    
    def get_llm_by_public_id(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get LLM by public_id as dictionary."""
        with self.session_scope() as session:
            llm = session.query(LLM).filter_by(public_id=public_id, is_active=True).first()
            return self._llm_to_dict(llm) if llm else None
    
    def get_llm_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get LLM by name as dictionary."""
        with self.session_scope() as session:
            llm = session.query(LLM).filter_by(name=name, is_active=True).first()
            return self._llm_to_dict(llm) if llm else None
    
    def get_all_llms(self) -> List[Dict[str, Any]]:
        """Get all active LLMs as dictionaries."""
        with self.session_scope() as session:
            llms = session.query(LLM).filter_by(is_active=True).all()
            return [self._llm_to_dict(llm) for llm in llms]
    
    def get_llms_by_provider(self, provider_public_id: str) -> List[Dict[str, Any]]:
        """Get all LLMs for a provider as dictionaries."""
        with self.session_scope() as session:
            provider = session.query(Provider).filter_by(public_id=provider_public_id, is_active=True).first()
            if not provider:
                return []
            
            llms = session.query(LLM).filter_by(provider_id=provider.id, is_active=True).all()
            return [self._llm_to_dict(llm) for llm in llms]
    
    def create_message(self, chat_public_id: str, user_public_id: str, content: str, role: str, llm_public_id: str) -> Dict[str, Any]:
        """Create a message and return as dictionary."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=chat_public_id, is_active=True).first()
            if not chat:
                raise NotFoundError("Chat not found")
            
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            llm = None
            if llm_public_id:
                llm = session.query(LLM).filter_by(public_id=llm_public_id, is_active=True).first()
                if not llm:
                    raise NotFoundError("LLM not found")
            
            message = Message(
                chat_id=chat.id,
                user_id=user.id,
                content=content,
                role=role,
                llm_id=llm.id if llm else None
            )
            session.add(message)
            session.flush()
            return self._message_to_dict(message)
    
    def update_message(self, public_id: str, content: str) -> Dict[str, Any]:
        """Update a message and return as dictionary."""
        with self.session_scope() as session:
            message = session.query(Message).filter_by(public_id=public_id, is_active=True).first()
            if not message:
                raise NotFoundError("Message not found")
            
            message.content = content
            session.add(message)
            return self._message_to_dict(message)
    
    def delete_message(self, public_id: str) -> None:
        """Delete a message."""
        with self.session_scope() as session:
            message = session.query(Message).filter_by(public_id=public_id, is_active=True).first()
            if not message:
                raise NotFoundError("Message not found")
            
            self.soft_delete(message)
    
    def get_message_by_public_id(self, public_id: str) -> Optional[Dict[str, Any]]:
        """Get message by public_id as dictionary."""
        with self.session_scope() as session:
            message = session.query(Message).filter_by(public_id=public_id, is_active=True).first()
            return self._message_to_dict(message) if message else None
    
    def get_messages_by_chat(self, chat_public_id: str) -> List[Dict[str, Any]]:
        """Get all messages for a chat as dictionaries."""
        with self.session_scope() as session:
            chat = session.query(Chat).filter_by(public_id=chat_public_id, is_active=True).first()
            if not chat:
                return []
            
            messages = session.query(Message)\
                .filter_by(chat_id=chat.id, is_active=True)\
                .order_by(Message.created_at.asc())\
                .all()
            return [self._message_to_dict(message) for message in messages]
    
    def enable_instruction_recording(self, user_public_id: str) -> Dict[str, Any]:
        """Enable instruction recording for a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            user.record_instructions = True
            session.add(user)
            return self._user_to_dict(user)
    
    def disable_instruction_recording(self, user_public_id: str) -> Dict[str, Any]:
        """Disable instruction recording for a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            user.record_instructions = False
            session.add(user)
            return self._user_to_dict(user)
    
    def get_user_instructions(self, user_public_id: str) -> List[Dict[str, Any]]:
        """List all instruction records for a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                return []
            
            records = session.query(InstructionRecord).filter_by(user_id=user.id).all()
            return [self._instruction_record_to_dict(record) for record in records]
    
    def record_instruction(self, user_public_id: str, chat_public_id: str, instruction: str) -> Dict[str, Any]:
        """Record an instruction for a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            chat = session.query(Chat).filter_by(public_id=chat_public_id, is_active=True).first()
            if not chat:
                raise NotFoundError("Chat not found")
            
            record = InstructionRecord(user_id=user.id, chat_id=chat.id, instruction=instruction)
            session.add(record)
            session.flush()
            return self._instruction_record_to_dict(record)
    
    def delete_instruction_records(self, user_public_id: str) -> None:
        """Delete all instruction records for a user."""
        with self.session_scope() as session:
            user = session.query(User).filter_by(public_id=user_public_id, is_active=True).first()
            if not user:
                raise NotFoundError("User not found")
            
            session.query(InstructionRecord).filter_by(user_id=user.id).delete()
    
    def get_instruction_records(self) -> List[Dict[str, Any]]:
        """List all instruction records."""
        with self.session_scope() as session:
            records = session.query(InstructionRecord).all()
            return [self._instruction_record_to_dict(record) for record in records]
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert user to dictionary."""
        return {
            'user_id': user.public_id,
            'username': user.username,
            'display_name': user.display_name,
            'profile': user.profile,
            'record_instructions': user.record_instructions,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }
    
    def _chat_to_dict(self, chat: Chat) -> Dict[str, Any]:
        """Convert chat to dictionary."""
        return {
            'chat_id': chat.public_id,
            'title': chat.title,
            'users': [self._user_to_dict(user) for user in chat.users],
            'messages': [self._message_to_dict(message) for message in chat.messages],
            'created_at': chat.created_at.isoformat(),
            'updated_at': chat.updated_at.isoformat()
        }
    
    def _message_to_dict(self, message: Message) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            'message_id': message.public_id,
            'chat_id': message.chat.public_id,
            'user_id': message.user.public_id if message.user else None,
            'llm_id': message.llm.public_id if message.llm else None,
            'content': message.content,
            'role': message.role,
            'created_at': message.created_at.isoformat(),
            'updated_at': message.updated_at.isoformat()
        }
    
    def _provider_to_dict(self, provider: Provider) -> Dict[str, Any]:
        """Convert provider to dictionary."""
        return {
            'provider_id': provider.public_id,
            'name': provider.name,
            'api_endpoint': provider.api_endpoint,
            'api_key': provider.api_key,
            'created_at': provider.created_at.isoformat(),
            'updated_at': provider.updated_at.isoformat()
        }
    
    def _llm_to_dict(self, llm: LLM) -> Dict[str, Any]:
        """Convert LLM to dictionary."""
        return {
            'llm_id': llm.public_id,
            'name': llm.name,
            'provider_id': llm.provider.public_id,
            'created_at': llm.created_at.isoformat(),
            'updated_at': llm.updated_at.isoformat()
        }
    
    def _instruction_record_to_dict(self, record: InstructionRecord) -> Dict[str, Any]:
        """Convert instruction record to dictionary."""
        return {
            'record_id': record.public_id,
            'user_id': record.user.public_id,
            'chat_id': record.chat.public_id,
            'instruction': record.instruction,
            'created_at': record.created_at.isoformat(),
            'updated_at': record.updated_at.isoformat()
        }