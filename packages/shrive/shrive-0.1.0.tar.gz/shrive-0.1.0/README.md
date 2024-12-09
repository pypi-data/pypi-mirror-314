# Shrive

"...in slaughterhouses far beyond their ken. I shed no tear for those that die *unshriven*...
For they are men. Just men. And what are men but chariots of wrath... by demons *driven."

Alan Moore is the greatest goddamn writer that ever graced the funny pages. Yeah, Gaiman, Morrison, Kiernan, Gillen, Spurrier - all good! All great! But Alan was something else.
And that is to say nothing of his Blakean epic *"Jerusalem"*, the post-hoc epitaph and exultation of his friend Steve *"Unearthing"* or the best representation of Tipheret put to paper *"Snakes & Ladders"*.

What does this have to do with this guy:
![Ferris the Rust Crab](https://rustacean.net/assets/rustacean-flat-happy.svg)

Well... nothing, positively fuck all. But I couldn't think of a better name than "shrive" (y'know, I'm German, we use that root as the regular word for *to write* ("schreiben")), for extracting text from the Andrew Lang fairy books.

And I wanted that for a multi-stage web project. I want to have a folder that I can *watchdog* and then have individual files for file-based routing. I really like the Python watchdog and this gives me the perfect excuse to try PyO3 (I saw it on **Developer Voices** and thought "Ooh, neat!" in a Margin Simpson voice). And with this crate I hope to leverage the *blazingly fast* execution of Rust/PyO3 with the commodity of the Python watchdog.

After the watchdog, I'll see about what web framework would be best for serving the files.
<!-- markdownlint-disable MD033 MD045 -->
> Current contenders:
>
> - <span style="display: inline-flex; align-items: center; gap: 4px;"><a href="https://astro.build/">Astro</a> <img src="https://astro.build/assets/press/astro-icon-dark.svg" height="20" alt="Astro Icon"/></span>
> - <span style="display: inline-flex; align-items: center; gap: 4px;"><a href="https://kit.svelte.dev/">SvelteKit</a> <img src="https://raw.githubusercontent.com/sveltejs/branding/master/svelte-logo.svg" height="20" alt="SvelteKit Logo"/></span>
> - <span style="display: inline-flex; align-items: center; gap: 4px;"><a href="https://zine-ssg.io/">Zine</a> <img src="https://ziglang.org/img/zig-logo-dark.svg" height="20" alt="Zine Icon"/></span>
<!-- markdownlint-enable MD033 MD045 -->

## Installation

```bash
pip install shrive
```
