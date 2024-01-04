import { Injectable } from "@angular/core";
import { Router } from "@angular/router";
import { knownFolders, ImageSource } from "@nativescript/core";
import { getJSON, HTTPFormData, HTTPFormDataEntry } from "@klippa/nativescript-http";
import { BASE_URL, SessionService } from "~/app/shared/auth/session.service";
import { DoorPrediction, PredictionResult } from "~/app/models/prediction";

@Injectable({providedIn: "root"})
export class ImageService {
  constructor(private router: Router, private sessionService: SessionService) {
  }

  imageSet: { front: string, back: string, side: string } = {front: undefined, back: undefined, side: undefined};
  predictedDoors: DoorPrediction[];
  isLoading: boolean = false;

  addImage(part: string, image: ImageSource) {
    const fileName = knownFolders.temp().path + part + ".jpg";
    image.saveToFile(fileName, "jpg");
    this.imageSet[part] = fileName;
  }

  clearImages() {
    for (let part in this.imageSet) {
      this.imageSet[part] = "";
    }
  }

  hasImages() {
    return Object.values(this.imageSet).every(value => !!value);
  }

  async sendPrediction() {
    this.isLoading = true;

    const formParams = new HTTPFormData();

    formParams.append("front", new HTTPFormDataEntry(new java.io.File(this.imageSet.front), this.imageSet.front, "image/jpg"));
    formParams.append("back", new HTTPFormDataEntry(new java.io.File(this.imageSet.back), this.imageSet.back, "image/jpg"));
    formParams.append("side", new HTTPFormDataEntry(new java.io.File(this.imageSet.side), this.imageSet.side, "image/jpg"));

    const httpOptions = {
      headers: {
        "Content-Type": "multipart/form-data",
        "Authorization": this.sessionService.bearerToken
      },
      method: "POST",
      url: BASE_URL + "predict",
      content: formParams
    };

    return getJSON<PredictionResult>(httpOptions)
      .then((result) => {
        this.predictedDoors = Object.keys(result)
          .sort((key1, key2) => result[key2] - result[key1])
          .map(key => ({ door: key, prediction: result[key] as number } as DoorPrediction));

        this.router.navigate(["/prediction"]);
      }).catch((err) => {
        console.log("error:", err);
      }).finally(() => {
        this.isLoading = false;
        // TODO: Remove temp files here
      });
  }
}
