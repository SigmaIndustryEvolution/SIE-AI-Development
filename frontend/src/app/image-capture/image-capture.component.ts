import { Component } from "@angular/core";

@Component({
  selector: "ns-image-capture",
  templateUrl: "./image-capture.component.html",
  styleUrls: ["./image-capture.component.css"],
})
export class ImageCaptureComponent {
  constructor() {}
  isLoading: boolean = false;

  onSendingPrediction(switchBool: boolean) {
    this.isLoading = switchBool;
  }
}
