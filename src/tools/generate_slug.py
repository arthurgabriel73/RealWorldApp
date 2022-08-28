def generate_slug(title: str = None) -> str:
    slug = title.lower()
    slug = slug.split(" ")
    slug = "-".join(slug)

    return slug
