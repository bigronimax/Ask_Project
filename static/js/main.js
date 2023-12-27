const buttons = document.getElementsByClassName("rating-section")
const counters = document.getElementsByClassName("counter")

for (let i = 0; i < buttons.length; i++) {
    const [like, dislike] = buttons[i].children;
    like.addEventListener('click', () => {
        counters[i].innerHTML = Number(counters[i].innerHTML) + 1;
    })
    dislike.addEventListener('click', () => {
        counters[i].innerHTML = Number(counters[i].innerHTML) - 1;
    })
}
