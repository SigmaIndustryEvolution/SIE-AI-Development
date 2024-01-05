import { Component } from "@angular/core";
import { ImageService } from "../view.service";
import { RouterExtensions } from "@nativescript/angular";

@Component({
  selector: "ns-prediction",
  templateUrl: "./prediction.component.html",
  styleUrls: ["./prediction.component.css"],
})
export class PredictionComponent {
  private threshHold:number = 80.00;
  isCertain:boolean;


  constructor(private router: RouterExtensions, private imageService: ImageService) {
    this.isCertain = this.probabilityThreshhold;
  }

  get selectedClass() {
    return this.imageService.prediction[0].class;
  };

  get selectedClassUpper(){
    return this.imageService.prediction[0].class.toUpperCase();
  }

  get probability() {
    return Math.round(this.imageService.prediction[0].certainty * 100.0);
  }

  get probabilityThreshhold(){
    console.log("Probability")
    console.log(this.imageService.prediction[0].certainty*100.0);
    console.log("Boolean")
    console.log(this.imageService.prediction[0].certainty*100.0> this.threshHold);
    return this.imageService.prediction[0].certainty*100.0 > this.threshHold;
  }

  viewNewPrediction() {
    this.router.navigate(["image-capture"], { clearHistory: true });
    this.imageService.clearImages();
  }
}
