import { SetStateAction, useState } from "react"
import { Button } from "@/components/ui/button"
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuRadioGroup,
    DropdownMenuRadioItem,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Settings } from "lucide-react"
import { ThemePresetDropdown } from "./themePresetDropdown"
import { ModeToggle } from "./modeToggle"

const themePresets = [
    { name: "Sunset Glow", color: "#FF6B6B" },
    { name: "Default", color: "#4A4A4A" },
    { name: "Underground", color: "#2E2E2E" },
    { name: "Rose Garden", color: "#D81B60" },
    { name: "Lake View", color: "#00C4B4" },
    { name: "Forest Whisper", color: "#2E7D32" },
    { name: "Ocean Breeze", color: "#1E88E5" },
    { name: "Lavender Dream", color: "#AB47BC" },
]

export function SettingsComponent() {
    const [selectedTheme, setSelectedTheme] = useState("Sunset Glow")

    const handleThemeChange = (value: string) => {
        setSelectedTheme(value)
        // Apply the selected theme color to the application (e.g., update CSS variables or context)
        const theme = themePresets.find(p => p.name === value)
        if (theme) {
            document.documentElement.style.setProperty("--theme-color", theme.color)
        }
    }

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon">
                    <Settings className="h-4 w-4" />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="w-56">
                <DropdownMenuLabel>Settings</DropdownMenuLabel>
                <DropdownMenuSeparator />
                Mode: <ModeToggle />
                <ThemePresetDropdown />
                <DropdownMenuSeparator />
                <DropdownMenuRadioGroup value="full" onValueChange={(value) => console.log(value)}>
                    <DropdownMenuLabel>Content layout:</DropdownMenuLabel>
                    <DropdownMenuRadioItem value="full">test</DropdownMenuRadioItem>
                    <DropdownMenuRadioItem value="centered">Centered</DropdownMenuRadioItem>
                </DropdownMenuRadioGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="text-red-600 focus:text-red-600">
                    Reset to Default
                </DropdownMenuItem>
            </DropdownMenuContent>
        </DropdownMenu>
    )
}