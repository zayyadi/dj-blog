import os
from whoosh import index
from whoosh.filedb.filestore import FileStorage as store
from whoosh.fields import Schema, TEXT, ID

# from whoosh.index import create_in
from whoosh.qparser import QueryParser

# Create a Whoosh schema
schema = Schema(
    id=ID(unique=True, stored=True),
    title=TEXT(stored=True),
    content=TEXT,
)

# Create the index
index_dir = "media/index"
if not index.exists_in(index_dir):
    index.create_in(index_dir, schema)


# def create_index(sender=None, **kwargs):
#     if not os.path.exists(index_dir):
#         os.mkdir(index_dir)
#         storage = store(index_dir)
#         ix = index.Index(storage, schema=schema, create=True)


# Update the index when a new post is added or updated
# def update_index(post):
#     ix = index.open_dir(index_dir)
#     writer = ix.writer()
#     writer.update_document(
#         id=str(post.id),
#         title=post.title,
#         slug=post.slug,
#         content=post.content,
#     )
#     writer.commit()


def update_index(post):
    ix = index.open_dir(index_dir)
    writer = ix.writer()
    writer.update_document(id=str(post.id), title=post.title, content=post.content)
    writer.commit()


# Perform a search
def search(query):
    ix = index.open_dir(index_dir)
    with ix.searcher() as searcher:
        query_parser = QueryParser("content", ix.schema)
        parsed_query = query_parser.parse(query)
        results = searcher.search(parsed_query)
        return results
