const loginsec = document.querySelector('.login-section')
const loginlink = document.querySelector('.login-link')
const registerlink = document.querySelector('.register-link')
const messageBox = document.querySelector('#message-box')

registerlink.addEventListener('click', ()=>{
    loginsec.classList.add('active')
})
loginlink.addEventListener('click', ()=>{
    loginsec.classList.remove('active')

    // Check if user is invalid and display error message
  if (userIsInvalid) {
    messageBox.innerHTML = 'Invalid user. Please try again.'
  }
  else{
    // User is valid, display success message
    messageBox.innerHTML = 'Login successful!'
  }
})
