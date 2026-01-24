import reflex as rx

config = rx.Config(
    app_name="app_fyf_sag",

    # Server configuration
    #frontend_port=3000,
    #backend_port=8000,
    
    #plugins=['reflex.plugins.sitemap.SitemapPlugin', 'reflex.plugins.sitemap.SitemapPlugin()'],
    disable_plugins=['reflex.plugins.sitemap.SitemapPlugin'],
)
