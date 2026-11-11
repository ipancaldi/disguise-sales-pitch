# Disguise sales experience

[Live site](https://ipancaldi.github.io/disguise-sales-pitch/) · [Pages CMS editor](https://app.pagescms.org/ipancaldi/disguise-sales-pitch/main) · [Draft preview](https://ipancaldi.github.io/disguise-sales-pitch/preview/)

## Update copy and imagery

Open the [Pages CMS editor](https://app.pagescms.org/ipancaldi/disguise-sales-pitch/main). **Home** opens with the hero title, intro and image at the top. Use the sidebar to edit another section. The four verticals are under **Our verticals**.

### Replace an image

1. Find the image field, such as **Hero image** on **Home**.
2. Click the trash icon (**Remove image**) beside the current image. This clears the field and keeps the original in the media library.
3. Click **Upload** and choose a JPG, PNG or WebP from your computer. To reuse an image from the library, click **Select** and choose it there.
4. Check the preview and update the image alt text and any photo credit when those fields are available.
5. Click **Save** to save the draft. Follow **Preview and publish** in the editor sidebar to review the page.

The repo owner can invite marketing collaborators by email. [Pages CMS collaborator instructions](https://pagescms.org/docs/configuration/collaborators/)

Use landscape photos for photo headers and transparent PNG or WebP for isolated hardware. The templates retain the image frames, responsive layout, original brand pictograms, map and interactive 3D logic. Text can wrap as it grows, so keep headlines close to the current length.

## Preview and publish

1. In Pages CMS, save the draft and choose **Preview and publish** in the sidebar. When the build finishes, open or refresh the preview. The **Draft preview** badge identifies the saved revision. [Draft preview](https://ipancaldi.github.io/disguise-sales-pitch/preview/) · [Build status](https://github.com/ipancaldi/disguise-sales-pitch/actions/workflows/publish.yml)
2. Review the page and share it with the publisher. The publisher opens a pull request from `main` into `production` and checks that the latest draft commit matches the preview badge. [Open a publishing pull request](https://github.com/ipancaldi/disguise-sales-pitch/compare/production...main?expand=1)
3. Select **Create a merge commit** on the pull request. GitHub updates the live site from `production`. Use merge commits so GitHub recognises which draft commits have already been published.

The preview is available to anyone with its link and asks search engines to skip indexing it. The repository and saved drafts are public.

## Local preview

With Python 3.12 and the dependencies in `site/requirements.txt`, run `python site/build.py` and open the generated `index.html`. Copy and image choices are stored in `content/`, uploaded imagery in `media/`, and protected templates in `site/`. The published HTML embeds its local assets and works offline; external links and hosted video remain online. GitHub retains the history of content changes for rollback.
