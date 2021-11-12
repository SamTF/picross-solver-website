<!-- JS -->
<script>
    export let grid_size = 4;
    export let board;

    $: col = `repeat(${grid_size}, 1fr)`;
	$: row = `repeat(${grid_size}, 1fr)`;
</script>


<!-- HTML -->
<div class="grid" style="grid-template-rows: {row}; grid-template-columns: {col};">
	{#key grid_size}
    {#each {length: grid_size} as _, row (row)}
        {#each {length: grid_size} as _, col (col)}
            <div class:filled={board[row][col]} class:empty={!board[row][col]}
                    on:contextmenu|preventDefault={console.log(row, col)}
                ></div>
        {/each}
    {/each}
	{/key}
</div>