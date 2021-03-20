$("#loginBtn").click(function() {

})
document.getElementById("loginBtn").addEventListener("click", () => {
	console.log("okay clicked");
	event.preventDefault()
	axios.post("/logi", {
		"username": document.getElementById("username").value,
		"pass": document.getElementById("pass").value
	}).then(res => {
		let isPWDValid = res.data.result
		if (isPWDValid === "true") {
			showFingerPrint()
		}
	}).catch(err => {
		console.log(err);
	})
})

function showFingerPrint() {
	$("#hideFingerPrint").removeClass("hideFingerPrint")
	$("#loginform").hide()
	$("#loginform").addClass("showFingerPrint")
	axios.post("/fingerpintverify", {}).then(res => {
		let authorizedUser = res.data.authorizedUser
		if (authorizedUser === "false") {
			makeFingerPrintError()
			console.log("make finger print");
		} else {
			location.reload()
		}
	}).catch(err => {
		console.log(err);
	})
}

function makeFingerPrintError() {
	$(".fa-fingerprint").css("color", "red")
	axios.post("/fingerpintverify", {}, {
		headers: {
			"Content-Type": "application/json"
		}
	}).then(res => {
		let authorizedUser = res.data.authorizedUser
		if (authorizedUser === "false") {
			makeFingerPrintError()
		}
	}).catch(err => {
		console.log(err);
	})
}