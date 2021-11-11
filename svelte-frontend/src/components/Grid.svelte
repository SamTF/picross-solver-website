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
                    on:click={() => console.log(row, col)}
                    on:mouseover={() => console.log(row, col)}
                    on:focus={() => console.log('whatever')}
                    on:contextmenu|preventDefault={console.log(row, col)}
                ></div>
        {/each}
    {/each}
	{/key}
</div>


<!-- CSS -->
<!-- <style>
	.grid-container {
		display: grid;
		border: 1px solid #999;
		border-radius: 2px;
		width: 300px;
		height: 300px;
		grid-gap: 1px;
		background: #999;
		margin-bottom: 1rem;
	} 
	
	.grid-container div {
		background: #fff;
	}	
	
	div.filled {
		background: orange;
	}
	div.empty {
		background: green;
	}
</style> -->