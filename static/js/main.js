function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const question_buttons = document.getElementsByClassName("question-rating-section")
const question_counters = document.getElementsByClassName("question-counter")

for (let i = 0; i < question_buttons.length; i++) {
    const [like, dislike] = question_buttons[i].children;
    like.addEventListener('click', () => {

        const formData = new FormData();
        
        formData.append("question_id", like.dataset.id)
        formData.append("like", 1)

        const request = new Request('/questionLike/', {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                question_counters[i].innerHTML = data.count
            });
    })
    dislike.addEventListener('click', () => {

        const formData = new FormData();

        formData.append("question_id", like.dataset.id)
        formData.append("like", 0)

        const request = new Request("/questionLike/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                question_counters[i].innerHTML = data.count
            });

    })
}

const answer_buttons = document.getElementsByClassName("answer-rating-section")
const answer_counters = document.getElementsByClassName("answer-counter")

for (let i = 0; i < answer_buttons.length; i++) {
    const [like, dislike] = answer_buttons[i].children;
    like.addEventListener('click', () => {

        const formData = new FormData();
        
        formData.append("answer_id", like.dataset.id)
        formData.append("like", 1)

        const request = new Request('/answerLike/', {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                answer_counters[i].innerHTML = data.count
            });
    })
    dislike.addEventListener('click', () => {

        const formData = new FormData();

        formData.append("answer_id", like.dataset.id)
        formData.append("like", 0)

        const request = new Request("/answerLike/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                answer_counters[i].innerHTML = data.count
            });

    })
}
