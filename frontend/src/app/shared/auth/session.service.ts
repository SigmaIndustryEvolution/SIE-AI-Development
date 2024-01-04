import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { firstValueFrom } from "rxjs";

export const BASE_URL = "https://safari-app1.digistrada.com/api/";
export const USERNAME = "joakimahlen";
export const PASSWORD = "zxc123!";

export interface User {
  roles: string[];
  name: string;
  id: number;
}

export interface AuthenticationResponse {
  claims: User;
  token: string;
}

@Injectable({providedIn: "root"})
export class SessionService {
  private currentUser?: User;
  private token?: string;

  constructor(private http: HttpClient) {
  }

  get bearerToken() {
    if (!this.token) {
      throw new Error("Not authenticated!");
    }

    return "Bearer " + this.token;
  }
  authenticate(): Promise<User | void> {
    const payload = {username: USERNAME, password: PASSWORD};

    return firstValueFrom(this.http.post<AuthenticationResponse>(BASE_URL + "authenticate", payload))
      .then((res) => {
        this.token = res.token;
        this.currentUser = res.claims;

        return this.currentUser;
      })
      .catch(err => {
        console.error("= Error authenticating!", err);

        throw err;
      });


  }
}
