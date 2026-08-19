import { Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import Analyses from "./pages/Analyses";
import AnalysisDetail from "./pages/AnalysisDetail";
import Home from "./pages/Home";
import Report from "./pages/Report";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />

        <Route path="/report" element={<Report />} />

        <Route path="/analyses" element={<Analyses />} />

        <Route path="/analyses/:analysisId" element={<AnalysisDetail />} />
      </Route>
    </Routes>
  );
}
