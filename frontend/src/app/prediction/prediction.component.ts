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

  get selectedDoor() {
    return this.imageService.predictedDoors[0].door;
  };

  get selectedDoorUpper(){
    return this.imageService.predictedDoors[0].door.toUpperCase();
  }

  get probability() {
    return Math.round(this.imageService.predictedDoors[0].prediction * 100.0);
  }

  get probabilityThreshhold(){
    console.log("Probability")
    console.log(this.imageService.predictedDoors[0].prediction*100.0);
    console.log("Boolean")
    console.log(this.imageService.predictedDoors[0].prediction*100.0> this.threshHold);
    return this.imageService.predictedDoors[0].prediction*100.0 > this.threshHold;
  }

  viewParts() {
    console.log("Door '" + this.selectedDoor + "' was predicted with " + this.probability + "% probability");
    this.router.navigate(["/" + this.selectedDoor ]);
  }

  viewNewPrediction() {
    this.router.navigate(["front"], { clearHistory: true });
    this.imageService.clearImages();
  }
}
