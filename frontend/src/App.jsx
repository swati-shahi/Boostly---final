import React, { useState, useEffect } from "react";
import axios from "axios";
import { Sparkles, Sun, BatteryMedium, ShieldCheck, Flame, Compass, ArrowRight, CheckCircle2, Moon } from "lucide-react";

const API_BASE = "http://127.0.0.1:8000/api/v1";

const CIRCADIAN_HOURS = [
  { hour: 8, energy: 3.2, tag: "Awakening" },
  { hour: 9, energy: 4.5, tag: "Prime Focus" },
  { hour: 10, energy: 4.8, tag: "Deep Zone" },
  { hour: 11, energy: 4.2, tag: "Execution" },
  { hour: 12, energy: 3.0, tag: "Rest & Nourish" },
  { hour: 13, energy: 2.5, tag: "Low Tide" },
  { hour: 14, energy: 2.2, tag: "Quiet Slump" },
  { hour: 15, energy: 3.1, tag: "Ascending" },
  { hour: 16, energy: 3.9, tag: "Second Flow" },
  { hour: 17, energy: 4.0, tag: "Integration" },
  { hour: 18, energy: 3.4, tag: "Unwind" },
];

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [burnoutData, setBurnoutData] = useState(null);
  const [energyLevel, setEnergyLevel] = useState(4);
  const [hoursWorked, setHoursWorked] = useState(5.5);

  useEffect(() => {
    fetchTasks();
    fetchBurnoutAssessment();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await axios.get(`${API_BASE}/tasks`);
      setTasks(res.data);
    } catch (err) {
      console.error("Failed fetching tasks", err);
    }
  };

  const fetchBurnoutAssessment = async () => {
    try {
      const res = await axios.get(`${API_BASE}/analytics/burnout-assessment`);
      setBurnoutData(res.data);
    } catch (err) {
      console.error("Failed fetching burnout data", err);
    }
  };

  const handleQuickLog = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    setLoading(true);
    try {
      await axios.post(`${API_BASE}/tasks/quick-log`, { raw_prompt: prompt });
      setPrompt("");
      await fetchTasks();
    } catch (err) {
      console.error("Task creation failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleRebalance = async () => {
    try {
      const res = await axios.post(`${API_BASE}/tasks/rebalance-circadian`);
      setTasks(res.data);
    } catch (err) {
      console.error("Circadian alignment failed", err);
    }
  };

  const handleLogEnergy = async () => {
    try {
      await axios.post(`${API_BASE}/telemetry/energy`, {
        hour_of_day: new Date().getHours(),
        energy_level: parseInt(energyLevel),
        hours_worked_today: parseFloat(hoursWorked),
      });
      await fetchBurnoutAssessment();
    } catch (err) {
      console.error("Telemetry failed", err);
    }
  };

  const deepWorkTasks = tasks.filter((t) => t.cognitive_load >= 0.6);
  const flowTasks = tasks.filter((t) => t.cognitive_load < 0.6);

  return (
    <div className="min-h-screen bg-[#fcfbf7] text-stone-800 p-6 md:p-12 selection:bg-amber-200 selection:text-stone-900">
      <div className="max-w-6xl mx-auto space-y-10">
        
        {/* Editorial Top Bar */}
        <header className="flex flex-col md:flex-row md:items-end justify-between pb-6 border-b border-stone-200/80 gap-6">
          <div className="space-y-1">
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-emerald-800">
              <Sun className="w-4 h-4 text-amber-500 fill-amber-400" /> Circadian Rhythm AI Engine
            </div>
            <h1 className="text-3xl md:text-4xl font-display font-bold tracking-tight text-stone-900">
              Boostly Studio
            </h1>
            <p className="text-stone-500 text-sm">
              Work when your mind is sharp. Rest before fatigue turns into friction.
            </p>
          </div>

          {/* Biological State Card */}
          {burnoutData && (
            <div className="flex items-center gap-4 bg-white px-5 py-3 rounded-2xl border border-stone-200/90 shadow-sm">
              <div className="p-2 bg-stone-100 rounded-xl">
                {burnoutData.burnout_detected ? (
                  <Flame className="w-5 h-5 text-rose-500" />
                ) : (
                  <ShieldCheck className="w-5 h-5 text-emerald-600" />
                )}
              </div>
              <div className="text-xs">
                <div className="font-semibold text-stone-800 flex items-center gap-1.5">
                  Burnout Risk Index: <span className="font-display font-bold">{(burnoutData.risk_score * 100).toFixed(0)}%</span>
                </div>
                <div className="text-stone-500 max-w-xs truncate">{burnoutData.message}</div>
              </div>
            </div>
          )}
        </header>

        {/* Motivational Zero-Friction Input Box */}
        <section className="bg-white p-2.5 rounded-2xl border border-stone-200/80 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.04)]">
          <form onSubmit={handleQuickLog} className="flex flex-col sm:flex-row items-center gap-2">
            <div className="relative flex-1 w-full">
              <Sparkles className="w-4 h-4 text-amber-600 absolute left-4 top-3.5" />
              <input
                type="text"
                placeholder="What's on your mind? (e.g., 'Finish research paper literature review, takes 2 hours')..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                className="w-full bg-stone-50/50 border border-transparent focus:border-stone-300 focus:bg-white rounded-xl pl-11 pr-4 py-3 text-sm text-stone-800 placeholder-stone-400 focus:outline-none transition"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full sm:w-auto px-6 py-3 bg-stone-900 hover:bg-stone-800 text-stone-100 font-medium text-xs tracking-wide rounded-xl transition flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? "Aligning..." : <>Decompose & Align <ArrowRight className="w-3.5 h-3.5" /></>}
            </button>
          </form>
        </section>

        {/* Tactile Circadian Wave Timeline */}
        <section className="bg-white border border-stone-200/80 rounded-2xl p-6 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-semibold tracking-wider uppercase text-stone-500">
              <Compass className="w-4 h-4 text-emerald-700" /> Circadian Energy Baseline
            </div>
            <button
              onClick={handleRebalance}
              className="text-xs font-semibold text-emerald-800 hover:text-emerald-900 flex items-center gap-1.5 transition underline underline-offset-4 decoration-emerald-200 hover:decoration-emerald-500"
            >
              Auto-Align to Peak Windows ↺
            </button>
          </div>

          <div className="grid grid-cols-11 gap-2 pt-3">
            {CIRCADIAN_HOURS.map((slot) => {
              const isPeak = slot.energy >= 4.0;
              const isDip = slot.energy <= 2.5;
              const heightPercent = (slot.energy / 5) * 100;

              return (
                <div key={slot.hour} className="flex flex-col items-center gap-1.5 text-center">
                  <span className="text-[11px] font-mono text-stone-400 font-medium">{slot.hour}:00</span>
                  <div className="w-full h-24 bg-stone-50 rounded-xl p-1 flex items-end justify-center border border-stone-100 relative group overflow-hidden">
                    <div
                      className={`w-full rounded-lg transition-all duration-300 ${
                        isPeak
                          ? "bg-amber-400/90"
                          : isDip
                          ? "bg-stone-200"
                          : "bg-emerald-300/80"
                      }`}
                      style={{ height: `${heightPercent}%` }}
                    />
                  </div>
                  <span className="text-[9px] font-medium text-stone-500 truncate max-w-full">
                    {slot.tag}
                  </span>
                </div>
              );
            })}
          </div>
        </section>

        {/* Clean Editorial Columns: Deep Focus vs Gentle Flow */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Deep Work Column */}
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-stone-200">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
                <h2 className="text-sm font-display font-bold text-stone-900 uppercase tracking-wide">
                  Deep Focus (Cognitive Load &ge; 60%)
                </h2>
              </div>
              <span className="text-xs font-mono text-stone-400 font-bold">{deepWorkTasks.length}</span>
            </div>

            {deepWorkTasks.length === 0 ? (
              <div className="p-8 text-center bg-stone-50/60 border border-dashed border-stone-200 rounded-2xl text-xs text-stone-400">
                Clear horizon. No heavy cognitive loads queued.
              </div>
            ) : (
              deepWorkTasks.map((task) => (
                <div key={task.id} className="bg-white border border-stone-200/90 hover:border-amber-400/80 rounded-2xl p-5 shadow-sm transition space-y-3">
                  <div className="flex justify-between items-start gap-2">
                    <h3 className="text-sm font-semibold text-stone-900 leading-snug">{task.title}</h3>
                    <span className="text-[11px] font-mono px-2 py-0.5 bg-amber-50 text-amber-800 border border-amber-200/60 rounded-md shrink-0">
                      {task.scheduled_hour ? `${task.scheduled_hour}:00` : "Prime Peak"}
                    </span>
                  </div>

                  {task.subtasks && task.subtasks.length > 0 && (
                    <div className="pt-2.5 border-t border-stone-100 space-y-1.5">
                      <span className="text-[10px] uppercase tracking-wider font-semibold text-stone-400">Decomposed Milestones</span>
                      {task.subtasks.map((st) => (
                        <div key={st.id} className="flex items-center justify-between text-xs text-stone-600 bg-stone-50/70 px-3 py-1.5 rounded-lg">
                          <span className="flex items-center gap-2">
                            <CheckCircle2 className="w-3.5 h-3.5 text-stone-400" /> {st.title}
                          </span>
                          <span className="text-[11px] font-mono text-stone-400">{st.estimated_minutes}m</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Gentle Flow Column */}
          <div className="space-y-4">
            <div className="flex items-center justify-between pb-2 border-b border-stone-200">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                <h2 className="text-sm font-display font-bold text-stone-900 uppercase tracking-wide">
                  Gentle Execution (Load &lt; 60%)
                </h2>
              </div>
              <span className="text-xs font-mono text-stone-400 font-bold">{flowTasks.length}</span>
            </div>

            {flowTasks.length === 0 ? (
              <div className="p-8 text-center bg-stone-50/60 border border-dashed border-stone-200 rounded-2xl text-xs text-stone-400">
                No low-friction chores waiting.
              </div>
            ) : (
              flowTasks.map((task) => (
                <div key={task.id} className="bg-white border border-stone-200/90 rounded-2xl p-5 shadow-sm space-y-2">
                  <div className="flex justify-between items-start gap-2">
                    <h3 className="text-sm font-medium text-stone-800">{task.title}</h3>
                    <span className="text-[11px] font-mono px-2 py-0.5 bg-stone-100 text-stone-600 rounded-md shrink-0">
                      {task.scheduled_hour ? `${task.scheduled_hour}:00` : "Low Slot"}
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Biometrics & Daily Recharge */}
          <div className="space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-stone-200">
              <span className="w-2.5 h-2.5 rounded-full bg-stone-400" />
              <h2 className="text-sm font-display font-bold text-stone-900 uppercase tracking-wide">
                Daily Check-in
              </h2>
            </div>

            <div className="bg-white border border-stone-200/90 rounded-2xl p-6 shadow-sm space-y-5 text-xs">
              <div>
                <div className="flex justify-between mb-2">
                  <span className="font-medium text-stone-600">Current Mental Energy</span>
                  <span className="font-display font-bold text-stone-900 text-sm">{energyLevel} / 5</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  value={energyLevel}
                  onChange={(e) => setEnergyLevel(e.target.value)}
                  className="w-full accent-stone-900 bg-stone-100 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between mb-2">
                  <span className="font-medium text-stone-600">Hours Invested Today</span>
                  <span className="font-display font-bold text-stone-900 text-sm">{hoursWorked} hrs</span>
                </div>
                <input
                  type="number"
                  step="0.5"
                  value={hoursWorked}
                  onChange={(e) => setHoursWorked(e.target.value)}
                  className="w-full bg-stone-50 border border-stone-200 rounded-xl px-3.5 py-2.5 text-stone-900 focus:outline-none focus:border-stone-400 font-medium"
                />
              </div>

              <button
                onClick={handleLogEnergy}
                className="w-full py-3 bg-stone-100 hover:bg-stone-200 text-stone-800 font-semibold rounded-xl border border-stone-200 transition text-xs"
              >
                Log Biometrics & Update Model
              </button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}