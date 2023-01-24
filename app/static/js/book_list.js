(function () {
  const btnsBuyBook = document.querySelectorAll(".btnBuyBook");

  let isbnBookSelected = null;
  const csrf_token = document.querySelector("[name='csrf-token']").value;

  btnsBuyBook.forEach((btn) => {
    btn.addEventListener("click", function () {
      isbnBookSelected = this.id;
      confirmPurchase();
    });
  });

  const confirmPurchase = async () => {
    Swal.fire({
        title: 'Do you confirm the purchase of the selected book?',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Buy',
        showLoaderOnConfirm: true,
      preConfirm: async () => {
        console.log(window.origin);
        return await fetch(`${window.origin}/BuyBook`, {
          method: "POST",
          mode: "same-origin",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "X-CSRF-TOKEN": csrf_token,
          },
          body: JSON.stringify({
            'isbn': isbnBookSelected,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              notificationSwal('Error', response.statusText, 'error', 'Close');
            }
            return response.json();
          })
          .then((data) => {
            if(data.success){
                notificationSwal('¡Success!', 'Book Purchased', 'success', '¡Ok!');
            }else{
                notificationSwal('¡Alert!', data.message, 'warning', 'Ok');
            }
          })
          .catch((error) => {
            notificationSwal('Error', error, 'error', 'Close');
          });
      },
      allowOutsideClick: () => false,
      allowEscapeKey: () => false,
    });
  };
})();
