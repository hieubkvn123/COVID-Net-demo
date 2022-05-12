jQuery(() => {
	$(".alert-close").click(() => {
		$(".alert").css("display", "none")
	})

	$(".modal-header .close").on("click", () => {
		$(".modal").modal("toggle")
	})
})