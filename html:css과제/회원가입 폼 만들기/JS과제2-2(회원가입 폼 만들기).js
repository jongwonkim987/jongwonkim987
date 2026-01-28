const result = document.getElementById('result');
const form = document.getElementById('form');

form.addEventListener('submit', function (event) {
  event.preventDefault();
  const user_id = event.target.elements.id.value;
  const user_pw1 = event.target.elements.pw1.value;
  const user_pw2 = event.target.elements.pw2.value;
  const user_name = event.target.elements.name.value;
  const user_phone = event.target.elements.phone.value;
  const user_position = event.target.elements.position.value;
  const user_email = event.target.elements.email.value;
  const user_gender = event.target.elements.gender.value;
  const user_intro = event.target.elements.intro.value;

  if (user_id.length < 6) {
    alert('아이디는 6자 이상이어야 합니다.');
    return;
  }
  if (user_pw1 !== user_pw2) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  form.style.display = 'none';

  // 결과 출력
  result.innerHTML = `
    <p>${user_id}님 환영합니다.</p>
    <p>이름: ${user_name}</p>
    <p>전화번호: ${user_phone}</p>
    <p>원하는 직무: ${user_position}</p>
    <p>이메일: ${user_email}</p>
    <p>성별: ${user_gender}</p>
    <p>자기소개: ${user_intro}</p>
  `;
});
