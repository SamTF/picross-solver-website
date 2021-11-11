<!-- # this is an example of fetching and displaying data from the Flask backend -->

<!-- JS -->
<script>
    let rand = -1

    const fetch_rand = () => {
        fetch("/rand")
            .then(data => data.text())
            .then(data => (rand = data))
    }
</script>


<!-- HTML -->
<div>
    <p>This button fetches a random number from the Flask backend</p>
    <button on:click={fetch_rand}>{rand}</button>
</div>


<!-- CSS -->
<style>
    div p {
        font-weight: 700;
    }

    button {
        color: #ff3e00;
        background-color: rgb(41, 41, 41);
        font-weight: 700;
        font-size: 2rem;
        border-radius: 0;
        border: 4px solid #ff3e00;
        width: 25%;
    }
</style>