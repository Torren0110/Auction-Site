const smallImgs = document.querySelectorAll('.smallImg');
const bigImg = document.getElementById('bigImg');
const bigImgLink = document.getElementById('bigImgLink');


smallImgs.forEach((img) => {
    img.addEventListener('click', (event) => {
        bigImg.src = img.src;
        bigImgLink.href = img.src
    });
});
