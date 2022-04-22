/**
 * 이메일 유효성 검사 함수
 */
function checkEmailDuplication() {
  const email = $('#inputEmail');
  const email_check = $('#email-check');

  const email_data = email.val();

  /**
   * ID, @, .(점) 이 세 가지가 반드시 포함되어야 하는 정규식
   */
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

/**
 * 이메일 형식에 문제가 있을 경우 나타낼 텍스트 관련 함수입니다.
 * @param message 사용할 exception 문구를 입력합니다.
 */
function exceptionEmailType(message) {
  const email = $('#inputEmail');
  const email_check = $('#email-check');
  email_check.show();
  email_check.html(message);
  email_check.css("color", "red");
  email.focus();
}

/**
 *비밀번호 유효성 검사 함수
 */
function checkPassword() {
  const pw = document.getElementById('pw').value;
  const pw2 = document.getElementById('pw2').value;
  const reg_check = document.getElementById('reg-check');
  const pw_check = document.getElementById('pw-check');

  /**
   * 특수 문자(!,@,#,$,%)를 포함한 8글자 이상 16글자 이하의 글자만 걸러내는 정규식입니다.
   */
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

/**
 * 회원 가입을 요청할 함수
 */
function requestSignUp() {
  const name = $('#inputName').val();
  const email = $('#inputEmail');
  const emailData = $('#inputEmail').val();
  const password = $('#pw').val();

  if (!email.attr("disabled")) {
    exceptionEmailType("사용하실 이메일을 확인해 주세요.");
    return;
  }

  /**
   * - 사용해도 되는 비밀번호인지 재확인
   */
  if (checkPassword()) {
    $.ajax({
      type: 'POST',
      url: '/auth/register',
      data: {
        name_give: name, email_give: emailData, password_give: password
      },
      success: function (response) {
        // 회원가입이 완료되면 로그인 페이지로 이동
        window.location.href = 'login';
      }
    });
  }
}


/**
 * 로그인 요청 함수
 */
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
      /**
       * 로그인 요청의 응답으로 생성된 토큰을 받는다.
       */
      token = response['Authorization'];
      // console.log(token);

    }, error: function () {
      const loginCheck = $('#login-check');
      loginCheck.show();
      loginCheck.html("이메일과 비밀번호를 확인해 주세요.");
      loginCheck.css("color", "red");
    }
  });

  /**
   * 생성된 토큰으로 메인 페이지로 넘어가게 한다.
   * 헤더에 발급받은 토큰을 넣어준다.
   */
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

/**
 * 회원가입 페이지로 이동하는 함수
 */
function redirectSignUp() {
  window.location.href = 'register';
}