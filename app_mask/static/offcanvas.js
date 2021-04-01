<!-- 最外层div：页面布局 -->
<div class="off-canvas-wrap" data-offcanvas>
  <!-- 内部元素: "工具栏" 内容 (图标, 链接, 描述内容等)-->
  <div class="inner-wrap">
    <nav class="tab-bar">
      <section class="left-small">
        <a class="left-off-canvas-toggle menu-icon" href="#"><span></span></a>
      </section>

      <section class="middle tab-bar-section">
        <h1 class="title">Off-canvas Example</h1>
      </section>
    </nav>

    <!-- 滑动菜单 -->
    <aside class="left-off-canvas-menu">
      <!-- Add links or other stuff here -->
      <ul class="off-canvas-list test">
        <li><label>Heading</label></li>
        <li><a href="#">Link 1</a></li>
        <li><a href="#">Link 2</a></li>
        ...
      </ul>
    </aside>

    <!-- 主要内容 -->
    <section class="main-section">
      <h3>Lorem Ipsum</h3>
      <p>....</p>
    </section>

    <!-- 关闭菜单 -->
    <a class="exit-off-canvas"></a>

  </div> <!-- 结束内部内容 -->
</div> <!-- 结束滑动菜单 -->

<!-- 初始化 Foundation JS -->
<script>
$(document).ready(function() {
    $(document).foundation();
})
</script>