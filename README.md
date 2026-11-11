# Disguise sales experience

[Live site](https://ipancaldi.github.io/disguise-sales-pitch/) · [Pages CMS editor](https://app.pagescms.org/ipancaldi/disguise-sales-pitch/main)

## Update copy and imagery

Open the [Pages CMS editor](https://app.pagescms.org/ipancaldi/disguise-sales-pitch/main). **Home** opens with the hero title, intro and image at the top. Use the sidebar to edit another section. The four verticals are under **Our verticals**.

### Replace an image

1. Find the image field, such as **Hero image** on **Home**.
2. Click the trash icon (**Remove image**) beside the current image. This clears the field and keeps the original in the media library.
3. Click **Upload** and choose a JPG, PNG or WebP from your computer. To reuse an image from the library, click **Select** and choose it there.
4. Check the preview and update the image alt text and any photo credit when those fields are available.
5. Click **Save** to publish your edits. Refresh the live site once the [publishing workflow](https://github.com/ipancaldi/disguise-sales-pitch/actions/workflows/publish.yml) is green.

The repo owner can [invite marketing collaborators by email](https://pagescms.org/docs/configuration/collaborators/). Saved edits in this public repository are intended for publication.

Use landscape photos for photo headers and transparent PNG or WebP for isolated hardware. The templates retain the image frames, responsive layout, original brand pictograms, map and interactive 3D logic. Text can wrap as it grows, so keep headlines close to the current length.

## Local preview

With Python 3.12 and the dependencies in `site/requirements.txt`, run `python site/build.py` and open the generated `index.html`. Copy and image choices are stored in `content/`, uploaded imagery in `media/`, and protected templates in `site/`. The published HTML embeds its local assets and works offline; external links and hosted video remain online. GitHub retains the history of content changes for rollback.
