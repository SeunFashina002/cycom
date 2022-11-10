let add_to_cart = document.getElementsByClassName("update-cart");

for (i = 0; i < add_to_cart.length; i++) {
  add_to_cart[i].addEventListener("click", function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;
    // console.log("product", productId, "action", action);

    if (user === "AnonymousUser") {
      addCookieItem(productId, action);
    } else {
      updateUserOrder(productId, action);
    }
  });
}

function addCookieItem(productId, action) {
  if (action == "add") {
    if (cart[productId] == undefined) {
      cart[productId] = { quantity: 1 };
    } else {
      cart[productId]["quantity"] += 1;
    }
  }

  if (action == "remove") {
    cart[productId]["quantity"] -= 1;
    if (cart[productId]["quantity"] <= 0) {
      delete cart[productId];
    }
  }
  console.log(cart);
  document.cookie =
    "cart=" + JSON.stringify(cart) + ";domain=;path=/;max-age=73737383939399";
  location.reload();
}

function updateUserOrder(productId, action) {
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
