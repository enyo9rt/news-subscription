function checkEmailDuplication() {
  const email = $('#inputEmail');
  const email_check = $('#email-check');

  const email_data = email.val();

  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;

  if (reg.test(email_data) === false) {
    exceptionEmailType("이메일 형식이 올바르지 않습니다.");
  } else {
    email_check.hide();
    $.ajax({
      type: 'POST',
      url: '/auth/register/email-check',
      data: {email_give: email_data},
      async: false,
      success: function (response) {
        email.attr("disabled", true);
      }, error: function () {
        exceptionEmailType("이미 사용 중인 이메일 입니다.");
      }
    });
  }
}

function exceptionEmailType(message) {
  const email = $('#inputEmail');
  const email_check = $('#email-check');
  email_check.show();
  email_check.html(message);
  email_check.css("color", "red");
  email.focus();
}

function checkPassword() {
  const pw = document.getElementById('pw').value;
  const pw2 = document.getElementById('pw2').value;
  const reg_check = document.getElementById('reg-check');
  const pw_check = document.getElementById('pw-check');
  const reg = /^(?=.*[a-zA-Z])((?=.*\d)(?=.*\W)).{8,16}$/;


  if (!reg.test(pw)) {
    reg_check.hidden = false
    pw_check.hidden = true

    reg_check.innerHTML = '비밀번호는 특수 문자(!,@,#,$,%)를 포함한 8글자 이상, 16글자 이하만 이용 가능합니다.'
    reg_check.style.color = 'red';
    return false;
  } else {
    reg_check.hidden = true
    pw_check.hidden = false

    if (pw !== '' && pw2 !== '') {
      if (pw === pw2) {
        pw_check.innerHTML = '비밀번호가 일치합니다.'
        pw_check.style.color = 'blue';
        return true;

      } else {
        pw_check.innerHTML = '비밀번호가 일치하지 않습니다.';
        pw_check.style.color = 'red';
        return false;
      }
    }
  }
}

function requestSignUp() {
  const name = $('#inputName').val();
  const email = $('#inputEmail');
  const emailData = $('#inputEmail').val();
  const password = $('#pw').val();

  if (!email.attr("disabled")) {
    exceptionEmailType("사용하실 이메일을 확인해 주세요.");
    return;
  }

  if (checkPassword()) {
    $.ajax({
      type: 'POST',
      url: '/auth/register',
      data: {name_give: name, email_give: emailData, password_give: password},
      success: function (response) {
        window.location.href = 'login';
      }
    });
  }
}

function requestSignIn() {
  const email = $('#login-email').val();
  const password = $('#login-password').val();
  let token = "";
  $.ajax({
    type: 'POST',
    url: '/auth/login',
    async: false,
    data: {email_give: email, password_give: password},
    success: function (response) {
      token = response['Authorization'];
      console.log(token);

    }, error: function () {
      const loginCheck = $('#login-check');
      loginCheck.show();
      loginCheck.html("이메일과 비밀번호를 확인해 주세요.");
      loginCheck.css("color", "red");
    }
  });

  $.ajax({
    type: 'GET',
    url: '/home',
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Content-type", "application/json");
      xhr.setRequestHeader("Authorization", token);
    },
    data: {},
    success: function () {
      window.location.href = '../../home';
    }, error: function () {

    }
  });


}

function redirectSignUp() {
  window.location.href = 'register';
}