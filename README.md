# Jootbuddy Books — website

Two static pages for Jootbuddy Books, an independent press, plus the order flow for its first release, *Escaping Samsara*.

Plain HTML and CSS. No framework, no build step, no JavaScript. Upload the folder to any static host and it works.

## Live

- **Site:** https://jootbuddybooks.com (also https://rumblebuffen.github.io/jootbuddy-books/)
- **Hosting:** GitHub Pages, from the repository https://github.com/Rumblebuffen/jootbuddy-books (branch `main`, root folder)
- **To change anything:** open the file on GitHub, click the pencil icon, edit, and commit. The site republishes itself in about a minute or two.
- `CNAME` holds the custom domain. Don't delete it.

> This folder sits inside the `distilled-markets-tools` repository for convenience, but it is independent of it: it shares no files with the Distilled Markets app and should be deployed on its own.

## Files

```
index.html                     home page
escaping-samsara.html          book page and order flow
css/styles.css                 all styling; the brand palette and type live in the :root block at the top
assets/
  escaping-samsara-cover.jpg   the cover, 1250 × 2000 JPG
  favicon.svg                  the mark, strokes thickened for tab size
  jootbuddy-mark-ink.svg       brand mark, ink on paper (from the brand kit)
  jootbuddy-mark-reversed.svg  brand mark, paper on ink (from the brand kit)
  fonts/                       self-hosted Hanken Grotesk and Libre Caslon (woff2)
scripts/watermark_pdf.py       stamps buyer name and order reference onto every page of a PDF
.nojekyll                      tells GitHub Pages to serve the files as-is
README.md                      this file
```

## Cover and social preview

- **Cover** is in place at `assets/escaping-samsara-cover.jpg` (1250 × 2000 JPG, made from the 1600 × 2560 PNG in the *Escaping Samsara Book* folder on the Desktop). The frame takes the image's own proportions, so nothing is cropped or letterboxed.
- **To replace it later:** on GitHub open the `assets` folder, click **Add file → Upload files**, upload a file named exactly `escaping-samsara-cover.jpg`, and commit. If the new cover has different proportions, also change the `width`/`height` attributes on the two `<img>` tags (currently `1250` × `2000`).
- **Link previews** (Substack, WhatsApp, Slack and the like) use the `og:image` tag in each page's `<head>`, which points at the live cover URL. Nothing to do unless the domain changes.

## Brand assets: already applied

The palette, fonts and mark from the brand kit are wired in. To change any of them:

- **Palette and type** are the `:root` block at the top of `css/styles.css`: ink `#16202E`, paper `#F6F1E8`, brass `#A6803C`, and the warm ink ramp for text. Change a value there and it changes everywhere. No colour or font is hardcoded in the HTML.
- **Fonts** live in `assets/fonts/`: Hanken Grotesk (interface and body), Libre Caslon Display (headings) and Libre Caslon Text (editorial serif and italic). All three are Open Font License, so self-hosting is fine. To swap fonts, drop new woff2 files in, update the `@font-face` blocks at the top of the CSS, and change the three `--font-*` variables.
- **The mark** is inlined as SVG in the header, the home-page masthead and the footer, so it takes its colour from the CSS variables (`currentColor` for the book and ring, `--accent` for the spine). The brand-kit SVG files are in `assets/` for use elsewhere, such as social avatars.
- **Favicon**: `assets/favicon.svg` is a standalone file, so it carries its own literal hex colours. Edit it separately if the palette changes.

## Editing the order details

- **Price** appears in three places: the home-page card, the book-page price block, and inside the pre-filled email body (`$18`). Search both HTML files for `18`.
- **Order email address**: search for `nat213@gmail.com`. It appears in the mailto links, the footers and the About section.
- **The pre-filled email** is the `href` of the "Email your order" button on the book page. It's a URL-encoded mailto (`%20` is a space, `%0D%0A` is a new line). The least error-prone way to change it is to regenerate the whole string:

  ```bash
  python3 -c 'import urllib.parse as u; print("mailto:nat213@gmail.com?subject=" + u.quote("Escaping Samsara — Order Request", safe="") + "&body=" + u.quote("Hi Nathan,\r\n\r\nYour new body text here.\r\n", safe=""))'
  ```

  Paste the output into the `href`, changing the single `&` before `body=` to `&amp;`.
- **Bank details never go in the page.** They go out by reply only. Keep it that way.

## Personalising each copy

`scripts/watermark_pdf.py` stamps "Licensed to NAME · Order REF · Please do not redistribute" in the footer of every page and writes the buyer, order reference and delivery date into the PDF's metadata.

```bash
pip install pypdf reportlab --break-system-packages
```

```bash
python3 scripts/watermark_pdf.py escaping-samsara.pdf "Buyer Name" JB-0001 escaping-samsara-JB-0001.pdf
```

The script covers the PDF only. Personalise the EPUB by whatever method you already use.

## Deploying

The folder is self-contained. Deploy **this folder**, not the parent repository.

### Netlify, drag and drop

1. Sign in at https://app.netlify.com and open https://app.netlify.com/drop.
2. Drag the whole `jootbuddy-books` folder onto the page.
3. It's live at a `something.netlify.app` address within seconds. To update, open the site's **Deploys** tab and drag the folder onto the deploy area again.

### GitHub Pages

1. Create a new public repository, for example `jootbuddy-books`.
2. Upload the **contents** of this folder to the repository root. `index.html` must be at the top level. The `.nojekyll` file is included so GitHub serves everything as-is.
3. In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a branch**. Choose branch `main`, folder `/ (root)`, and save.
4. The site appears at `https://USERNAME.github.io/jootbuddy-books/` after a minute or two. Each later commit republishes automatically.

### Pointing a custom domain at it

You'll need two places open: the DNS settings wherever you bought the domain, and the host's domain settings.

**Netlify**

1. Site → **Domain management → Add a domain**, and enter your domain.
2. In your DNS, add an `A` record for the root (`@`) pointing at Netlify's load balancer (`75.2.60.5` at the time of writing; Netlify shows the current value in the same screen) and a `CNAME` record for `www` pointing at your `something.netlify.app` address. Or move the nameservers to Netlify DNS, which sets this up for you.
3. Netlify issues the HTTPS certificate automatically once DNS resolves, usually within an hour.

**GitHub Pages**

1. Repository → **Settings → Pages → Custom domain**. Enter the domain and save. GitHub adds a `CNAME` file to the repository.
2. In your DNS, add four `A` records for the root pointing at `185.199.108.153`, `185.199.109.153`, `185.199.110.153` and `185.199.111.153`, plus a `CNAME` for `www` pointing at `USERNAME.github.io`.
3. Back in **Settings → Pages**, tick **Enforce HTTPS** once the DNS check passes.

DNS changes can take up to a day to reach everyone, though it's usually under an hour.
