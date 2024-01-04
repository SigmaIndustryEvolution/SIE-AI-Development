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

  imageSet: { view1: string 
    // view2: string, 
    // view3: string 
   } 
    = {view1: undefined
      // , view2: undefined
      // , view3: undefined
    };

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

    formParams.append("view1", new HTTPFormDataEntry(new java.io.File(this.imageSet.view1), this.imageSet.view1, "image/jpg"));

    // formParams.append("view2", new HTTPFormDataEntry(new java.io.File(this.imageSet.view2), this.imageSet.view2, "image/jpg"));
    // formParams.append("view3", new HTTPFormDataEntry(new java.io.File(this.imageSet.view3), this.imageSet.view3, "image/jpg"));

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
