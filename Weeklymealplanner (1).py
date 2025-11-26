import React, { useState, useEffect } from 'react';
import { Trash2, ShoppingCart, Plus, X, Save, ChefHat } from 'lucide-react';

// --- Constants & Configuration ---
const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
const MEAL_TYPES = ["Breakfast", "Lunch", "Dinner"];

export default function App() {
  // State for meal data
  const [mealData, setMealData] = useState({});
  
  // State for Modal (Editor)
  const [isEditorOpen, setIsEditorOpen] = useState(false);
  const [editingSlot, setEditingSlot] = useState({ day: null, type: null });
  const [editName, setEditName] = useState("");
  const [editIngredients, setEditIngredients] = useState("");

  // State for Shopping List Modal
  const [isShoppingListOpen, setIsShoppingListOpen] = useState(false);
  const [shoppingList, setShoppingList] = useState([]);

  // Load data from LocalStorage on mount
  useEffect(() => {
    const savedData = localStorage.getItem("meal_plan_data");
    if (savedData) {
      try {
        setMealData(JSON.parse(savedData));
      } catch (e) {
        console.error("Failed to load data", e);
      }
    }
  }, []);

  // Save data to LocalStorage whenever it changes
  useEffect(() => {
    localStorage.setItem("meal_plan_data", JSON.stringify(mealData));
  }, [mealData]);

  // --- Actions ---

  const openEditor = (day, type) => {
    const currentMeal = mealData[day]?.[type] || { name: "", ingredients: "" };
    setEditingSlot({ day, type });
    setEditName(currentMeal.name);
    setEditIngredients(currentMeal.ingredients);
    setIsEditorOpen(true);
  };

  const saveMeal = () => {
    const { day, type } = editingSlot;
    const newData = { ...mealData };
    
    if (!newData[day]) newData[day] = {};
    
    newData[day][type] = {
      name: editName.trim(),
      ingredients: editIngredients.trim()
    };

    setMealData(newData);
    setIsEditorOpen(false);
  };

  const clearWeek = () => {
    if (window.confirm("Are you sure you want to delete all meals?")) {
      setMealData({});
    }
  };

  const generateShoppingList = () => {
    const allIngredients = [];
    
    Object.values(mealData).forEach(dayMeals => {
      Object.values(dayMeals).forEach(meal => {
        if (meal.ingredients) {
          // Split by comma, clean whitespace, and capitalize
          const items = meal.ingredients.split(',').map(i => {
            const trimmed = i.trim();
            return trimmed.charAt(0).toUpperCase() + trimmed.slice(1);
          }).filter(i => i);
          allIngredients.push(...items);
        }
      });
    });

    if (allIngredients.length === 0) {
      alert("No ingredients found! Add some meals first.");
      return;
    }

    // Deduplicate and sort
    const uniqueItems = [...new Set(allIngredients)].sort();
    setShoppingList(uniqueItems);
    setIsShoppingListOpen(true);
  };

  const copyToClipboard = () => {
      const text = "SHOPPING LIST\n=============\n\n" + shoppingList.map(item => `- ${item}`).join('\n');
      const textarea = document.createElement("textarea");
      textarea.value = text;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand('copy');
        alert("Copied to clipboard!");
      } catch (err) {
        console.error('Unable to copy', err);
      }
      document.body.removeChild(textarea);
  };

  // --- Render Helpers ---

  const getSlotContent = (day, type) => {
    const meal = mealData[day]?.[type];
    if (meal && meal.name) {
      return (
        <div className="flex flex-col items-center justify-center h-full w-full">
          <span className="font-semibold text-gray-800 text-center text-sm md:text-base">{meal.name}</span>
          {meal.ingredients && (
             <span className="text-[10px] text-gray-400 mt-1 hidden sm:block">Has ingredients</span>
          )}
        </div>
      );
    }
    return (
      <div className="flex items-center justify-center h-full text-gray-400 hover:text-green-600 transition-colors">
        <Plus size={18} className="mr-1" />
        <span className="text-sm font-medium">Add</span>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#f4f6f9] font-sans text-slate-700 p-4 md:p-8">
      
      {/* Header */}
      <header className="max-w-6xl mx-auto mb-8 text-center">
        <div className="flex items-center justify-center mb-2">
            <div className="bg-white p-3 rounded-full shadow-sm mr-3">
                <ChefHat className="text-green-600" size={32} />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-[#2c3e50]">Weekly Meal Planner</h1>
        </div>
        <p className="text-slate-500">Plan your week, save money, eat better.</p>
      </header>

      {/* Main Grid */}
      <main className="max-w-6xl mx-auto bg-white rounded-xl shadow-lg overflow-hidden border border-slate-200">
        
        {/* Desktop/Tablet Table Layout */}
        <div className="grid grid-cols-[100px_1fr_1fr_1fr] divide-x divide-y divide-slate-200 border-b border-slate-200">
            {/* Header Row */}
            <div className="bg-[#2c3e50] text-white p-4 font-bold flex items-center justify-center">Day</div>
            {MEAL_TYPES.map(type => (
                <div key={type} className="bg-[#2c3e50] text-white p-4 font-bold text-center">{type}</div>
            ))}

            {/* Data Rows */}
            {DAYS.map(day => (
                <React.Fragment key={day}>
                    <div className="bg-slate-50 p-4 font-bold text-[#2c3e50] flex items-center justify-center border-r border-slate-200">
                        {day}
                    </div>
                    {MEAL_TYPES.map(type => (
                        <div key={`${day}-${type}`} className="p-1 h-24 md:h-32 bg-white hover:bg-green-50 transition-colors relative group">
                            <button 
                                onClick={() => openEditor(day, type)}
                                className="w-full h-full rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50"
                            >
                                {getSlotContent(day, type)}
                            </button>
                        </div>
                    ))}
                </React.Fragment>
            ))}
        </div>
      </main>

      {/* Footer Buttons */}
      <footer className="max-w-6xl mx-auto mt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
        <button 
            onClick={clearWeek}
            className="flex items-center px-6 py-3 bg-red-500 hover:bg-red-600 text-white rounded-lg shadow transition-colors font-semibold"
        >
            <Trash2 size={20} className="mr-2" />
            Clear Week
        </button>

        <button 
            onClick={generateShoppingList}
            className="flex items-center px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow-md transition-colors font-bold text-lg"
        >
            <ShoppingCart size={24} className="mr-2" />
            Generate Shopping List
        </button>
      </footer>

      {/* --- Modals --- */}

      {/* Meal Editor Modal */}
      {isEditorOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="bg-[#2c3e50] p-4 flex justify-between items-center">
                <h3 className="text-white font-bold text-lg">Edit {editingSlot.day} - {editingSlot.type}</h3>
                <button onClick={() => setIsEditorOpen(false)} className="text-white hover:text-red-300">
                    <X size={24} />
                </button>
            </div>
            
            <div className="p-6 space-y-4">
                <div>
                    <label className="block text-sm font-bold text-gray-700 mb-1">Meal Name</label>
                    <input 
                        type="text" 
                        value={editName}
                        onChange={(e) => setEditName(e.target.value)}
                        placeholder="e.g. Scrambled Eggs"
                        className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all"
                        autoFocus
                    />
                </div>
                
                <div>
                    <label className="block text-sm font-bold text-gray-700 mb-1">Ingredients</label>
                    <span className="text-xs text-gray-500 block mb-2">Separate items with commas (e.g. Eggs, Milk, Salt)</span>
                    <textarea 
                        value={editIngredients}
                        onChange={(e) => setEditIngredients(e.target.value)}
                        placeholder="List your ingredients here..."
                        className="w-full p-3 border border-gray-300 rounded-lg h-32 focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none transition-all resize-none"
                    />
                </div>

                <button 
                    onClick={saveMeal}
                    className="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg shadow transition-colors flex justify-center items-center"
                >
                    <Save size={20} className="mr-2" />
                    Save Meal
                </button>
            </div>
          </div>
        </div>
      )}

      {/* Shopping List Modal */}
      {isShoppingListOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl w-full max-w-md max-h-[80vh] flex flex-col animate-in fade-in zoom-in duration-200">
                <div className="bg-green-600 p-4 flex justify-between items-center rounded-t-xl shrink-0">
                    <h3 className="text-white font-bold text-lg flex items-center">
                        <ShoppingCart size={20} className="mr-2" /> Shopping List
                    </h3>
                    <button onClick={() => setIsShoppingListOpen(false)} className="text-white hover:text-green-200">
                        <X size={24} />
                    </button>
                </div>

                <div className="p-6 overflow-y-auto grow bg-slate-50">
                    {shoppingList.length > 0 ? (
                        <ul className="space-y-2">
                            {shoppingList.map((item, idx) => (
                                <li key={idx} className="flex items-center p-3 bg-white rounded shadow-sm border border-slate-100">
                                    <input type="checkbox" className="w-5 h-5 text-green-600 rounded border-gray-300 focus:ring-green-500 mr-3 cursor-pointer" />
                                    <span className="text-gray-700 text-lg">{item}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-center text-gray-500 italic">Your list is empty.</p>
                    )}
                </div>

                <div className="p-4 border-t border-gray-200 shrink-0 bg-white rounded-b-xl">
                    <button 
                        onClick={copyToClipboard}
                        className="w-full py-3 bg-[#2c3e50] hover:bg-slate-700 text-white font-bold rounded-lg transition-colors"
                    >
                        Copy to Clipboard
                    </button>
                </div>
            </div>
        </div>
      )}
    </div>
  );
}