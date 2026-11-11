# Disguise sales experience

[Live site](https://ipancaldi.github.io/disguise-sales-pitch/) · [Pages CMS editor](https://app.pagescms.org/)

## Update copy and imagery

1. Open Pages CMS and choose **ipancaldi / disguise-sales-pitch**, branch **main**.
2. Choose a section. The four verticals are under **Our verticals**; the hero title, intro and photo are under **Home**.
3. Edit the labelled text fields. Use an image field to upload or choose a JPG, PNG or WebP, then update the image description and any photo credit.
4. Select **Save**. GitHub rebuilds and publishes the page. Refresh the live site once the [publishing workflow](https://github.com/ipancaldi/disguise-sales-pitch/actions/workflows/publish.yml) is green.

The first time, the repo owner installs the [Pages CMS GitHub App](https://pagescms.org/docs/quick-start/) for this repository only. They can then [invite marketing collaborators by email](https://pagescms.org/docs/configuration/collaborators/). Saved edits in this public repository are intended for publication.

Use landscape photos for photo headers and transparent PNG or WebP for isolated hardware. The templates retain the image frames, responsive layout, original brand pictograms, map and interactive 3D logic. Text can wrap as it grows, so keep headlines close to the current length.

## Local preview

With Python 3.12 and the dependencies in `site/requirements.txt`, run `python site/build.py` and open the generated `index.html`. Copy and image choices are stored in `content/`, uploaded imagery in `media/`, and protected templates in `site/`. The published HTML embeds its local assets and works offline; external links and hosted video remain online. GitHub retains the history of content changes for rollback.
