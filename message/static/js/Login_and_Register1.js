const forms = document.querySelector(".forms"),
pwShowHide = document.querySelectorAll(".eye-icon"),
links = document.querySelectorAll(".link");

pwShowHide.forEach(eyeIcon => {
eyeIcon.addEventListener("click", () => {
  let pwFields = eyeIcon.parentElement.parentElement.querySelectorAll(".password");
  pwFields.forEach(password => {
      if(password.type === "password"){
          password.type = "text";
          eyeIcon.classList.replace("bx-hide", "bx-show");
          return;
      }
      password.type = "password";
      eyeIcon.classList.replace("bx-show", "bx-hide");
  })
})
})      

links.forEach(link => {
link.addEventListener("click", e => {
 e.preventDefault(); //preventing form submit
 forms.classList.toggle("show-signup");
})
})



// for login vaalidation

document.getElementById("loginForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submissio
  // / Get form values
  var email = document.getElementById("email").value.trim();
  var password = document.getElementById("password").value.trim();

  // Reset error messages
  document.getElementById("emailError").textContent = "";
  document.getElementById("passwordError").textContent = "";
  // Validate email
  if (email === "") {
    document.getElementById("emailError").textContent = "email is required.";
    document.getElementById("email").style.borderColor = "red";
  }
  // Validate password
  if (password === "") {
    document.getElementById("passwordError").textContent = "Password is required.";
    document.getElementById("password").style.borderColor = "red";
  }
  
});
// for register vaalidation

document.getElementById("registerForm").addEventListener("submit", function(event) {
  event.preventDefault(); // Prevent form submissio
  // / Get form values
  var email = document.getElementById("emailr").value.trim();
  var password = document.getElementById("passwordr").value.trim();
  var confirmPassword = document.getElementById("confirmPassword").value.trim();

  // Reset error messages
  document.getElementById("emailErrorr").textContent = "";
  document.getElementById("passwordErrorr").textContent = "";
  document.getElementById("confirmPasswordError").textContent = "";


  // Validate email
  if (email === "") {
    document.getElementById("emailErrorr").textContent = "email is required.";
    document.getElementById("emailr").style.borderColor = "red";
  }
  // Validate password
  if (password === "") {
    document.getElementById("passwordErrorr").textContent = "Password is required.";
    document.getElementById("passwordr").style.borderColor = "red";
  }
  if (confirmPassword !== password) {
    document.getElementById("confirmPasswordError").textContent = "Password is does not match.";
    // document.getElementById("confirmPassword").style.borderColor = "red";
  }
});

