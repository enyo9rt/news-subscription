function checkEmailDuplication() {
  console.log("중복 검사 시작")

  return true;
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
  } else {
    reg_check.hidden = true
    pw_check.hidden = false

    if (pw !== '' && pw2 !== '') {
      if (pw === pw2) {
        pw_check.innerHTML = '비밀번호가 일치합니다.'
        pw_check.style.color = 'blue';
      } else {
        pw_check.innerHTML = '비밀번호가 일치하지 않습니다.';
        pw_check.style.color = 'red';
      }
    }
  }
}