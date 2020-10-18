<script>
  import { onMount } from "svelte";
</script>

<main>
  <div class="column left">
     <slot name="left_content"></slot>
  </div>
  <div class="column right">
     <slot name="right_content"></slot>
  </div>
</main>

<style>
    * { 
        -moz-box-sizing: border-box; 
        -webkit-box-sizing: border-box; 
         box-sizing: border-box; 
    }

    main {
      height: 100%;
      background-color: #000;
      color: #fff;
    }

    .column {
      float: left;
      height: 100%;
      padding: 0 2em;
      display: flex;
      flex-flow: column wrap;
      overflow: hidden;
    }
    
    .left {
      width: 29%;
      background-color: #333;
      margin-right: 0.5%;
    }
    
    .right {
      width: 68%;
      background-color: #555;
    }

    @media (max-width: 640px) {
      main {
        max-width: none;
      }
      .column {
        display: block;
        float: false;
        width: 100%;
        height: auto;
      }
      .left {
        margin: auto;
        margin-bottom: 1%;
      }
    }
</style>
