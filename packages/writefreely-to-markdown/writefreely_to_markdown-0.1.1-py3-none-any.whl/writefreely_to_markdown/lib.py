from tomlkit import document
from tomlkit import table
from tomlkit import TOMLDocument
from tomlkit import dump
from datetime import datetime
from typing import List
import os


class frontmatter:
    # See https://www.getzola.org/documentation/content/page/#front-matter
    # This is an in-complete version of it.
    @staticmethod
    def get_frontmatter(
        title: str,
        description: str | None,
        date: datetime,  # Creation date,
        updated: datetime,
        draft: bool,
        slug: str,
        authors: List[str],
        # taxonomies
        tags: List[str],
        language: str,
    ) -> TOMLDocument:
        doc = document()
        # Ugly but works
        doc.add("title", title)  # type: ignore[arg-type]
        if description is not None:
            doc.add("description", description)  # type: ignore[arg-type]
        doc.add("date", date)  # type: ignore[arg-type]
        doc.add("updated", updated)  # type: ignore[arg-type]
        doc.add("draft", draft)  # type: ignore[arg-type]
        doc.add("slug", slug)  # type: ignore[arg-type]
        doc.add("authors", authors)  # type: ignore[arg-type]

        taxonomies = table()
        taxonomies.add("tags", tags)
        taxonomies.add("language", language)
        doc.add("taxonomies", taxonomies)
        return doc

    @staticmethod
    def get_description_from_body(body: str, tags=None) -> str | None:
        res = body.split("<!--more-->", 2)
        if len(res) < 2:
            return None

        if tags is not None:
            for tag in tags:
                res = res[0].split("#" + tag)

        stripped_res = res[0].replace(".\n\n", ". ").replace("\n\n", ". ").strip()

        # In case the result is empty
        if not stripped_res:
            return None
        else:
            return stripped_res

    @staticmethod
    def get_content_from_body(body: str) -> str:
        return body.split("<!--more-->")[-1].strip()


def write_json_as_markdown(json_obj, output_dir: str):
    os.mkdir(output_dir)
    collections = json_obj["collections"]
    for collection in collections:
        posts = collection["posts"]
        os.mkdir(os.path.join(output_dir, collection["alias"]))

        write_posts(posts, output_dir, collection["alias"])

    os.mkdir(os.path.join(output_dir, "draft_author"))
    write_posts(json_obj["posts"], output_dir, "draft_author")


def write_posts(posts, output_dir, author):
    for post in posts:
        if post["slug"] is None or len(post["slug"]) == 0:
            post["slug"] = post["id"]
            post["draft"] = True
        else:
            post["draft"] = False

        assert post["slug"] is not None

        out_path = os.path.join(output_dir, author, post["slug"] + ".md")

        # print(out_path)
        with open(out_path, mode="w") as write_fp:
            print(out_path)
            post_frontmatter = frontmatter.get_frontmatter(
                post["title"],
                frontmatter.get_description_from_body(post["body"], post["tags"]),
                post["created"],
                post["updated"],
                post["draft"],
                post["slug"],
                author,
                post["tags"],
                post["language"],
            )
            write_fp.write("+++\n")
            dump(post_frontmatter, write_fp)
            write_fp.write("+++\n")
            write_fp.write(frontmatter.get_content_from_body(post["body"]))
