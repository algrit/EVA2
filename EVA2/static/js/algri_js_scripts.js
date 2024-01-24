const testAttemptStartModal = document.getElementById('testAttemptStartModal')
if (testAttemptStartModal) {
  testAttemptStartModal.addEventListener('show.bs.modal', event => {
    // Link that triggered the modal
    const link = event.relatedTarget
    // Extract info from data-bs-* attributes
    const test_name = link.getAttribute('data-bs-test_name')
    // If necessary, you could initiate an Ajax request here
    // and then do the updating in a callback.

    // Update the modal's content.
    const modalText = testAttemptStartModal.querySelector('.modal-algri')

    modalText.textContent = `You are trying to start "${test_name}" Test Quiz.`
  })
}