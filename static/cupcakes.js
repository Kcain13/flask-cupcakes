const BASE_URL = 'http://localhost:5000/api';

/** generate html for given cupcake */

function generateCupcakeHTML(cupcake) {
    return `
    <div data-cupcake-id=${cupcake.id}>
    <li>
      ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
      <button class='delete-button'>Delete</button>
    </li>
    <img class="Cucpake-img"
         src="${cupcake.image}"
         alt="(no image provided)">
    </div>
    `;
}

/** put initial cupcakes on page */

async function showInitialCupcakes() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $("#cupcakes-list").append(newCupcake);
    }
}


/** handle form for adding of new cupcakes */

$("#new-cupcake-form").on("submit", async function (e) {
    e.preventDefault();

    let flavor = $("#form-flavor").val();
    let rating = $("#form-rating").val();
    let size = $("#form-size").val();
    let image = $("#form-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    })

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcakes-list').append(newCupcake);
    $('#new-cupcake-form').trigger("reset");
})

/** handle clicking delete */

$("cupcakes-list").on("click", ".delete-button", async function (e) {
    e.preventDefault();
    let $cupcake = $(e.target).closest('div');
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
})

$(showInitialCupcakes);