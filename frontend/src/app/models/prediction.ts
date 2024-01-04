export type DoorType = "alpha-microrib" | "condoor-st3v" | "crawford-542" | "hormann-spu40" | "novoferm-t45";
export type PredictionResult = { [key in DoorType]: number };
export type DoorPrediction = { door: DoorType, prediction: number };
