import { Injectable, ViewContainerRef } from "@angular/core";

@Injectable({ providedIn: "root" })
export class UIService {
  private _rootVCRef: ViewContainerRef;

  setRootVCRef(vcRef: ViewContainerRef) {
    this._rootVCRef = vcRef;
  }

  getRootVCref() {
    return this._rootVCRef;
  }
}
