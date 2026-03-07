<script>
</script>

<span class="blinking-cursor"><slot>█</slot></span>

<style>
    @-webkit-keyframes blinker {
      50% {
        visibility: hidden;
      }
    }
    .blinking-cursor{
      -webkit-animation: blinker 1s step-start 0s infinite;
    }
</style>
