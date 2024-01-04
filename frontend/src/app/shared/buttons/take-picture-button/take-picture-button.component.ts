import { Component, EventEmitter, Input, Output } from "@angular/core";
import * as camera from "@nativescript/camera";
import { ImageSource } from "@nativescript/core";
import { ImageService } from "../../../view.service";
import { requestCameraPermissions } from "@nativescript/camera";
import { RouterExtensions } from "@nativescript/angular";

@Component({
  selector: "ns-take-picture-button",
  templateUrl: "./take-picture-button.component.html",
  styleUrls: ["./take-picture-button.component.css"],
})
export class TakePictureButtonComponent {
  imageTaken = false;
  constructor(
    private imageService: ImageService,
    private router: RouterExtensions,
  ) {}
  @Output() sendingPrediction = new EventEmitter<boolean>();
  @Input() part: string = "";
  @Input() forwardPath: string = "";

  setImage() {
    requestCameraPermissions().then(() => {
      camera.takePicture({ saveToGallery: false }).then((imageAsset) => {
        ImageSource.fromAsset(imageAsset).then((imgSrc) => {
          if (imgSrc) {
            this.imageService.addImage(this.part, imgSrc);
            this.imageTaken = true;
            if(this.imageTaken && this.imageService.hasImages()){
              this.sendingPrediction.emit(true);
              this.imageService.sendPrediction();
              this.imageTaken = false;
            }
            else if (this.imageTaken) {
              this.router.navigate([this.forwardPath]);
              this.imageTaken = false;
            }
          } else {
            alert("Image source is bad");
            this.imageTaken = false;
          }
        });
      });
    });
    this.sendingPrediction.emit(false);
  }
}
