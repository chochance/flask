console.log("JavaScript 파일이 로드되었습니다.");

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    console.log("로그인 폼 제출 이벤트가 발생했습니다.");

    event.preventDefault(); // 기본 동작 막기
    const user_id = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log("입력된 user_id:", user_id);
    console.log("입력된 password:", password);

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id, password }),
        });

        const result = await response.json();
        console.log("서버 응답:", result);

        if (response.ok && result.success) {
            window.location.href = result.redirect_url;
        } else {
            document.getElementById("error-message").style.display = "block";
        }
    } catch (error) {
        console.error("로그인 요청 중 오류 발생:", error);
    }
});
