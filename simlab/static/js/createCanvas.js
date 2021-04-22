function createCanvas(width, height, set2dTransform = true) {
    const ratio = Math.ceil(window.devicePixelRatio);
    const canvas = document.createElement('canvas');
    canvas.style.width= `${width}px`;
    canvas.style.height=`${height}px`;
    canvas.width = width * ratio;
    canvas.height = height * ratio;
    if (set2dTransform) {
      canvas.getContext('2d').setTransform(ratio, 0, 0, ratio, 0, 0);
    }
    return canvas;
}
