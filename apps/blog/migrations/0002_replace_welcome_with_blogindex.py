from django.db import migrations

def replace_welcome_with_blogindex(apps, schema_editor):
    # Get models from apps to avoid import issues in migrations
    BlogIndexPage = apps.get_model('blog', 'BlogIndexPage')
    Site = apps.get_model('wagtailcore', 'Site')
    Page = apps.get_model('wagtailcore', 'Page')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Get the default site (usually there's only one)
    site = Site.objects.all().first()
    if not site:
        print("No site found, skipping migration.")
        return

    # Get the current root page of the site
    root_page = Page.objects.get(id=site.root_page_id)

    # Find the "Welcome to Wagtail" page, which should be a child of root with slug 'home'
    try:
        welcome_page = Page.objects.get(path__startswith=root_page.path, slug='home')
    except Page.DoesNotExist:
        print("No welcome page found, skipping replacement.")
        return

    # Prepare content type for BlogIndexPage
    blog_index_ct = ContentType.objects.get_for_model(BlogIndexPage)

    # Copy fields from welcome page for path, depth, etc.
    new_page_fields = {
        'id': welcome_page.id,  # Reuse the same id so it replaces it cleanly
        'path': welcome_page.path,
        'depth': welcome_page.depth,
        'numchild': welcome_page.numchild,
        'translation_key': welcome_page.translation_key,
        'locale_id': welcome_page.locale_id,
        'title': 'Blog',
        'draft_title': 'Blog',
        'slug': welcome_page.slug,
        'content_type': blog_index_ct,
        'live': welcome_page.live,
        'url_path': welcome_page.url_path,
    }

    # Delete the old welcome page
    welcome_page.delete()

    # Create the new BlogIndexPage using the reused fields
    new_blog_index_page = BlogIndexPage(**new_page_fields)
    new_blog_index_page.save()

    # Set the site's root page to the new BlogIndexPage
    site.root_page = new_blog_index_page
    site.save()

    print("Replaced welcome page with BlogIndexPage as root child.")

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),  # adjust to your latest migration of blog app
        ('wagtailcore', '__latest__'),
    ]

    operations = [
        migrations.RunPython(replace_welcome_with_blogindex),
    ]
