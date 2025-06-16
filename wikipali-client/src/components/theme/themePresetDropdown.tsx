import { SetStateAction, useState } from "react"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"

const themePresets = [
    { value: "sunset-glow", label: "Sunset Glow", color: "#FF6B6B" },
    { value: "default", label: "Default", color: "#4A4A4A" },
    { value: "underground", label: "Underground", color: "#2E2E2E" },
    { value: "rose-garden", label: "Rose Garden", color: "#D81B60" },
    { value: "lake-view", label: "Lake View", color: "#00C4B4" },
    { value: "forest-whisper", label: "Forest Whisper", color: "#2E7D32" },
    { value: "ocean-breeze", label: "Ocean Breeze", color: "#1E88E5" },
    { value: "lavender-dream", label: "Lavender Dream", color: "#AB47BC" },
]

export function ThemePresetDropdown() {
    const [selectedTheme, setSelectedTheme] = useState("sunset-glow")

    const handleValueChange = (value: SetStateAction<string>) => {
        setSelectedTheme(value)
        // Apply the selected theme color to the application (e.g., update CSS variables)
        document.documentElement.style.setProperty("--theme-color", themePresets.find(p => p.value === value).color)
    }

    return (
        <div className="space-y-2">
            <label htmlFor="theme-preset" className="text-sm font-medium">
                Theme preset:
            </label>
            <Select value={selectedTheme} onValueChange={handleValueChange}>
                <SelectTrigger id="theme-preset" className="w-[200px]">
                    <SelectValue placeholder="Select a theme" />
                </SelectTrigger>
                <SelectContent>
                    {themePresets.map((preset) => (
                        <SelectItem
                            key={preset.value}
                            value={preset.value}
                            className="flex items-center"
                        >
                            <span
                                className="w-3 h-3 mr-2 rounded-full"
                                style={{ backgroundColor: preset.color }}
                            />
                            {preset.label}
                        </SelectItem>
                    ))}
                </SelectContent>
            </Select>
        </div>
    )
}