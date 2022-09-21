let add_to_cart = document.getElementsByClassName("update-cart");

for (i = 0; i < add_to_cart.length; i++) {
  add_to_cart[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    // console.log("product", productId, "action", action);

    if (user === "AnonymousUser") {
      log("Not logged in");
    } else {
      updateUserFunction(productId, action);
    }
  });
}

function updateUserFunction(productId, action) {
  console.log("sending data...");
  let url = "/update-item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log("data: ", data);
      location.reload();
    });
}
