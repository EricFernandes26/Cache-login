var formSignin = document.querySelector('#signin')
var formSignup = document.querySelector('#signup')
var btnColor = document.querySelector('.btnColor')

// Manipulação de exibição dos formulários de Sign in e Sign up
document.querySelector('#btnSignin').addEventListener('click', () => {
    formSignin.style.left = "25px"
    formSignup.style.left = "450px"
    btnColor.style.left = "0px"
})

document.querySelector('#btnSignup').addEventListener('click', () => {
    formSignin.style.left = "-450px"
    formSignup.style.left = "25px"
    btnColor.style.left = "110px"
})

// Função para lidar com o login
document.getElementById("signin").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = event.target.querySelector("input[placeholder='Email']").value;
    const password = event.target.querySelector("input[placeholder='Password']").value;

    const response = await fetch("http://127.0.0.1:5000/signin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, password: password })
    });

    const result = await response.json();
    console.log(result); // Log da resposta para depuração

    if (response.ok) {
        // Redireciona para a página de boas-vindas após o login bem-sucedido
        window.location.href = "/welcome.html";
    } else {
        alert(result.error);
    }
});

// Função para lidar com o cadastro de usuário
document.getElementById("signup").addEventListener("submit", async function(event) {
    event.preventDefault();

    const email = event.target.querySelector("input[placeholder='Email']").value;
    const password = event.target.querySelectorAll("input[placeholder='Password']")[0].value;
    const confirmPassword = event.target.querySelectorAll("input[placeholder='Password']")[1].value;

    const response = await fetch("http://127.0.0.1:5000/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email: email, password: password, confirm_password: confirmPassword })
    });

    const result = await response.json();
    console.log(result); // Log da resposta para depuração

    if (response.ok) {
        alert(result.message);
    } else {
        alert(result.error);
    }
});
