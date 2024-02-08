from typing import Literal
import pytest
from django.db import IntegrityError
from blog import models


@pytest.mark.dbfixture
@pytest.mark.parametrize(
    "id,title,author,content,image,publish,status,slug,category,likes,snippet",
    [
        (
            1,
            "Create building heavy year.",
            1,
            "City task front natural scientist project unit. Space community nation Democrat. Tax clear pay anyone at.",
            "images/default.png",
            "2020-04-09 08:45:11.269818",
            "published",
            "short-authority",
            1,
            [],
            "Picture after notice month institution number.",
        ),
        (
            2,
            "Job pick you nothing.",
            1,
            "Edge explain language strong edge over much town. Change defense read lose class. Food wide ten word include control else model.",
            "images/default.png",
            "2020-09-10 12:34:43.953892",
            "draft",
            "art-summer-ability",
            1,
            [],
            "General contain side production improve.",
        ),
    ],
)
def test_blog_article_dbfixture(
    db: None,
    db_fixture_setup: None,
    id: Literal[1, 2],
    title: Literal["Create building heavy year.", "Job pick you nothing."],
    author: Literal[1],
    content: Literal[
        "City task front natural scientist project unit. Sp…",
        "Edge explain language strong edge over much town. …",
    ],
    image: Literal["images/default.png"],
    publish: Literal["2022-09-25T04:36:59.490556", "2020-09-02T14:56:17.820791"],
    status: Literal["published", "draft"],
    slug: Literal["short-authority", "art-summer-ability"],
    category: Literal[1],
    likes: list[int],
    snippet: Literal[
        "Picture after notice month institution number.",
        "General contain side production improve.",
    ],
):
    result = models.Article.objects.get(id=id)
    print(f"result: {result}")
    assert result.title == title
    assert result.author.id == author
    assert result.content == content
    assert result.image == image
    assert result.publish.strftime("%Y-%m-%d %H:%M:%S.%f") == publish
    assert result.status == status
    assert result.slug == slug
    assert result.category.id == category
    assert [like.id for like in result.likes.all()] == likes
    # assert result.likes.id == likes
    assert result.snippet == snippet


def test_blod_db_article_insert_data(
    db: None,
    article_factory,
):
    result = article_factory.create(
        title="title",
        author__id=3,
        content="content",
        image="images/default.png",
        publish="2020-04-09 08:45:11.269818",
        status="published",
        slug="slug",
        category__id=4,
        # likes__id=set(),
        snippet="snippet",
    )
    assert result.title == "title"
    assert result.author.id == 3
    assert result.content == "content"
    assert result.image == "images/default.png"
    assert result.publish == "2020-04-09 08:45:11.269818"
    assert result.status == "published"
    assert result.slug == "slug"
    assert result.category.id == 4
    # assert result.likes.id == set()
    assert result.snippet == "snippet"
