from haystack import indexes
from .models import Post


# Step 1 - in settings.py add 'haystack' as installed app and configure it for Solr for instance
# Step 2 - create a search_indexes.py - named like this by convention to allow Haystack
#          to automatically pick it up. In it put all Models that need to be indexed
# Step 3 - for the Post model create PostIndex(indexes.SearchIndex, indexes.Indexable) class
#          that defines 'get_model' method
# Step 4 - create a template file 'search/indexes/blog/post_text.txt' in the template directory
# Step 5 - build the Solr schema.xml. Use the Haystack command:
#          python manage.py build_solr_schema

class PostIndex(indexes.SearchIndex, indexes.Indexable):

    # Every SearchIndex requires there be one (and only one) field with document=True.
    # This indicates to both Haystack and the search engine about which field is
    # the primary field for searching within.
    # When you choose a document=True field, it should be consistently named across
    # all of your SearchIndex classes to avoid confusing the backend.
    # The convention is to name this field text.
    text = indexes.CharField(document=True, use_template=True)

    # In addition, we added several other fields (published).
    # These are useful when you want to provide additional filtering options.
    # Haystack comes with a variety of SearchField classes to handle most types of data.
    published = indexes.DateTimeField(model_attr='published')

    def get_model(self):
        return Post.published

    # A common theme is to allow admin users to add future content
    # but have it not display on the site until that future date is reached.
    # We specify a custom index_queryset method to prevent those future items from being indexed.
    def index_queyset(self, using=None):
        #  we'll use the custom 'status_published' query Manager
        return self.get_model().status_published.all()
