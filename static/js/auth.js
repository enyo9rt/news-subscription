function checkEmailDuplication() {
  const email = $('#inputEmail');
  const email_check = $('#email-check');

  const email_data = email.val();

  const reg = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;

  if (reg.test(email_data) === false) {
    email_check.show();
    email_check.html("이메일 형식이 올바르지 않습니다.");
    email_check.css("color", "red");
    email.focus();

  } else {
    email_check.hide();

    $.ajax({
      type: 'POST',
      url: '/auth/register/email-check',
      data: {email_give: email_data},
      async: false,
      success: function (response) {
        email.attr("disabled", true);
      }
    });
  }
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

function signUpProcess() {
  if (checkPassword()) {
    const name = $('#inputName').val();
    const email = $('#inputEmail').val();
    const password = $('#pw').val();

    console.log(name, email, password);
    $.ajax({
      type: 'POST',
      url: '/auth/register',
      data: {name_give: name, email_give: email, password_give: password},
      success: function (response) {
        console.log("회원 가입 결과: " + response)
      }
    });
  }
}