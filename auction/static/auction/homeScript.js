const toTopBtn = document.getElementById('toTopBtn');
const search = document.getElementById('search');
const searchSuggestion = document.getElementById('suggetions');

window.addEventListener('scroll', (event) => {
    if (!document.documentElement.scrollTop) {
        toTopBtn.classList.remove("visible");
        toTopBtn.classList.add("invisible");
    }
    else {
        toTopBtn.classList.remove("invisible");
        toTopBtn.classList.add("visible");
    }
})

toTopBtn.addEventListener('click', (event) => {
    window.scrollTo(0, 0);
})

search.addEventListener('focusin', (e) => {
    searchSuggestion.classList.remove('d-none');
});

search.addEventListener('focusout', (e) => {
    searchSuggestion.classList.add('d-none');
    if(search.value == "")
        searchSuggestion.innerHTML = '';
});

search.addEventListener('input', (e) => {
    if(search.value)
    {
        $.ajax({
            url: '/getSearch/',
            type: 'get',
            data: {text: search.value},
            success: (response) => {
                if(response)
                {
                    var output = "<ul>";
                    
                    response.forEach(item => {
                        output += `<li>${item}</li>`;
                    });

                    output += '</ul>';
                    searchSuggestion.innerHTML = output;
                }
                else{
                    searchSuggestion.innerHTML = "nothing";
                }
            }
        });
    }

});