(() => {
    const images = document.querySelectorAll(".doc-post img");
    if (!images.length) return;

    const dialog = document.createElement("dialog");
    dialog.className = "figure-lightbox";
    dialog.setAttribute("aria-label", "Expanded figure");
    dialog.innerHTML = `
        <div class="figure-lightbox__panel">
            <button class="figure-lightbox__close" type="button" aria-label="Close expanded figure">&times;</button>
            <img class="figure-lightbox__image" alt="">
            <p class="figure-lightbox__caption"></p>
        </div>`;
    document.body.append(dialog);

    const popupImage = dialog.querySelector(".figure-lightbox__image");
    const popupCaption = dialog.querySelector(".figure-lightbox__caption");
    const closeButton = dialog.querySelector(".figure-lightbox__close");

    const cleanText = (value) => value.replace(/\s+/g, " ").trim();

    const captionElementFor = (image) => {
        const paragraph = image.closest("p");
        if (!paragraph) return null;

        const copy = paragraph.cloneNode(true);
        copy.querySelectorAll("img").forEach((item) => {
            const wrapper = item.closest("span");
            (wrapper || item).remove();
        });
        const inlineCaption = cleanText(copy.textContent);
        if (inlineCaption) return paragraph;

        const next = paragraph.nextElementSibling;
        if (next?.matches("p")) {
            const nextText = cleanText(next.textContent);
            if (/^(figure|fig\.|table)\s*\d/i.test(nextText)) return next;
        }

        return null;
    };

    const captionFor = (image) => {
        const caption = captionElementFor(image);
        return caption ? cleanText(caption.textContent) : image.alt || "";
    };

    const openFigure = (image) => {
        popupImage.src = image.currentSrc || image.src;
        popupImage.alt = image.alt || "Expanded article figure";
        const caption = captionFor(image);
        popupCaption.textContent = caption;
        popupCaption.hidden = !caption;
        dialog.showModal();
        closeButton.focus();
    };

    images.forEach((image, index) => {
        const figureBlock = image.closest("p");
        const caption = captionElementFor(image);
        figureBlock?.classList.add("figure-block");
        if (caption) {
            caption.classList.add("figure-caption");
            if (caption === figureBlock) caption.classList.add("figure-caption--inline");
        }

        if (document.querySelector(".omsa-post") && caption) {
            const label = [...caption.querySelectorAll("span")]
                .find((span) => /^\s*Figure\s+\d+/i.test(span.textContent));
            if (label) label.textContent = `Figure ${index + 1}—`;
        }

        image.classList.add("figure-lightbox-trigger");
        image.tabIndex = 0;
        image.setAttribute("role", "button");
        image.setAttribute("aria-label", `${image.alt || "Article figure"}. Open enlarged view`);
        image.addEventListener("click", () => openFigure(image));
        image.addEventListener("keydown", (event) => {
            if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                openFigure(image);
            }
        });
    });

    closeButton.addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
        if (event.target === dialog) dialog.close();
    });
})();
