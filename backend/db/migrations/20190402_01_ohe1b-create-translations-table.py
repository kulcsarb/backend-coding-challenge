"""
create translations table
"""

from yoyo import step

__depends__ = {}

steps = [
    step("""
        CREATE TABLE translations (            
            id varchar PRIMARY KEY,
            sid varchar,            
            text text,
            translation text,
            source_language varchar(2),
            target_language varchar(2),
            status varchar,                    
            created_at timestamp without time zone DEFAULT now(),
            updated_at timestamp without time zone DEFAULT now()
            );
        CREATE INDEX translations_sid_idx on translations (sid);        
        CREATE INDEX translations_status_idx on translations (status);
        CREATE INDEX translations_source_idx on translations (source_language);
        CREATE INDEX translations_target_idx on translations (target_language);        
    """),
]
